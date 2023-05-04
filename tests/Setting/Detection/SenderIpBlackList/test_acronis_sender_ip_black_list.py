# TODO
# TODO Tests for all sections(admin user)
# TODO Settings-->Detection
# TODO  ADD+EDIT+DELETE

# TODO git ignore LogFiles and reports
# from urllib import request

import allure

from TestBuildingBlocks.SettingsDetection.test_setting_detection_items_list import TestSettingDetectionItemList
from pages.Settings.Detection.SettingsDetection_SenderIP_BlackList_Page import \
    SettingsDetectionSenderIpBlackListPage
from test_base import BaseTest


# Test Flow:

# 1.add two mails
# 2.verify 2 mails added
# 3.search for one
# 4.verify one
# 5.edit it
# 6.delete 2 mails
# 7.verify no bad request
# 8.verify correct url
class TestsSettingDetectionIpBlackListSenderAcronis(BaseTest):

    # Test Case in TestTrail direct link
    @allure.testcase('https://perceptionpointtemp.testrail.io/index.php?/cases/view/2343')
    # issue in JIRA direct link(bugs+todo items)
    # issue:
    @allure.issue("https://perception-point.atlassian.net/browse/MS-8798")
    @allure.description('log to chrome and record video of the test')
    def test_ip_address_black_list_acronis(self, setup_browser_page, read_non_secrets):
        page = setup_browser_page
        params_dictionary = read_non_secrets
        base_url = params_dictionary.get("ACRONIS_BASE_URL")

        settings_detection_black_list_sender_IP_page = SettingsDetectionSenderIpBlackListPage(page, base_url,
                                                                                              is_acronis=True)
        test_setting_detection_black_list_ip = TestSettingDetectionItemList(
            page
            , settings_detection_black_list_sender_IP_page
            , params_dictionary=params_dictionary
            , is_acronis=True
        )
        test_setting_detection_black_list_ip.setup_tear_down_gui_operations.login(page)
        test_setting_detection_black_list_ip.click_setting_menu_item_and_verify_url(page)

        test_setting_detection_black_list_ip.add_two_items_to_list(is_ip_blacklist_address=True)

        test_setting_detection_black_list_ip.get_number_of_added_items_and_assert(2)

        test_setting_detection_black_list_ip.search_for_items_and_assert_search_results_number(
            test_setting_detection_black_list_ip.ip_address1, 1)

        test_setting_detection_black_list_ip.edit_and_save_changes(test_setting_detection_black_list_ip.ip_address1)
        # setting_detection_page.click_cancel_search()
        test_setting_detection_black_list_ip.cancel_search()
        # Delete added mails
        test_setting_detection_black_list_ip.delete_two_list_items()
