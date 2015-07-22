from django.utils.datastructures import MultiValueDict as MultiDict

from sheerlike import filters


class TestArgParsing(object):

    def setup(self):
        self.args = MultiDict([('filter_category', ['cats', 'dogs']),
                               ('filter_planet', ['earth']),
                               ('filter_range_date_lte', ['2014-6-1']),
                               ('filter_range_comment_count_gt', ['100'])])

    def test_args_to_filter_dsl(self):
        filter_dsl = filters.filter_dsl_from_multidict(self.args)
        # the existing tests here seemed to depend of the other
        # of dictionary keys, which is undefined

    def test_range_args(self):
        filter_dsl = filters.filter_dsl_from_multidict(self.args)
        assert('range' in filter_dsl[1])
        assert('date' in filter_dsl[1]['range'])
        assert('comment_count' in filter_dsl[1]['range'])
        assert('2014-6-1' == filter_dsl[1]['range']['date']['lte'])
        assert('100' == filter_dsl[1]['range']['comment_count']['gt'])

    def test_filters_for_field(self):
        selected = filters.selected_filters_from_multidict(
            self.args, 'category')
        assert (('cats') in selected)
        assert (('dogs') in selected)


class TestDateValidation(object):

    def test_date_validation_incorrect_range(self):
        args = MultiDict([('filter_range_date_gte', ['2014-6']),
                          ('filter_range_date_lte', ['2013-6'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        assert(filter_dsl[0]['range']['date']['gte'] == '2013-6-1')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-30')

    def test_date_validation_correct_range(self):
        args = MultiDict([('filter_range_date_gte', ['2013-6']),
                          ('filter_range_date_lte', ['2014-6'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        assert(filter_dsl[0]['range']['date']['gte'] == '2013-6-1')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-30')

    def test_date_validation_with_days_correct_range(self):
        args = MultiDict([('filter_range_date_gte', ['2014-1-23']),
                          ('filter_range_date_lte', ['2014-6-23'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        assert(filter_dsl[0]['range']['date']['gte'] == '2014-1-23')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-23')

    def test_date_validation_with_days_incorrect_range(self):
        args = MultiDict([('filter_range_date_gte', ['2014-6-23']),
                          ('filter_range_date_lte', ['2014-1-23'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        assert(filter_dsl[0]['range']['date']['gte'] == '2014-1-23')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-23')

    def test_default_days_correct_range(self):
        args = MultiDict([('filter_range_date_gte', ['2014-1']),
                          ('filter_range_date_lte', ['2014-6'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        assert(filter_dsl[0]['range']['date']['gte'] == '2014-1-1')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-30')

    def test_default_days_incorrect_range(self):
        args = MultiDict([('filter_range_date_gte', ['2014-6']),
                          ('filter_range_date_lte', ['2014-1'])])
        filter_dsl = filters.filter_dsl_from_multidict(args)
        #from nose.tools import set_trace;set_trace()
        assert(filter_dsl[0]['range']['date']['gte'] == '2014-1-1')
        assert(filter_dsl[0]['range']['date']['lte'] == '2014-6-30')
