import os

from EmailWizard.CompleteIntegration.complete_gmail_configuration_page import CompleteGmailConfigurationPage
from EmailWizard.new_mail_service_wizard_page import NewMailServiceWizardPage
from EmailWizard.test_new_mail_service import TestBaseNewMailService
from SetupTearDownOperations.setup_teardown_gui_operations import SetupTearDownGuiOperations
from Utils.Assertions.mail_wizard_assertions import acronis_assertions
from pages.EmailWizard.new_service_add_domain_page import NewServiceWizardAddDomain
from pages.EmailWizard.verify_domain_page import verify_domain
from pages.EmailWizard.view_status_page import view_status


class TestGmailNewMailService(TestBaseNewMailService):
    def __init__(self, params_dictionary, is_acronis, is_accounts, service_type):
        self.user_licenses_per_domain = '10'
        self.is_accounts = is_accounts
        self.params_dictionary = params_dictionary
        self.service_type = service_type
        self.is_acronis = is_acronis

        if is_acronis:
            self.acronis_organization_id = params_dictionary.get("ACRONIS_ORGANIZATION_ID1")
            self.base_url = params_dictionary.get("ACRONIS_BASE_URL")
            self.acronis_token_value = os.getenv("ACRONIS_USER_TOKEN1")
        else:
            self.xray_organization_id = params_dictionary.get("XRAY_ORGANIZATION_ID")
            self.base_url = params_dictionary.get("XRAY_BASE_URL")
            self.xray_token_value = os.getenv("XRAY_USER_TOKEN1")

        self.service_type = service_type
        super().__init__(self.params_dictionary, self.is_acronis, self.is_accounts, self.service_type,
                         self.user_licenses_per_domain)

    def test_gmail_new_mail_service_wizard_start_page(self, page):
        self.test_new_mail_service_goto_menu_wizard_page(page)
        my_gmail_wizard_page = NewMailServiceWizardPage(page, self.is_acronis)
        my_gmail_wizard_page.click_gmail_service()
        my_gmail_wizard_page.click_next_button_enable(self.GMAIL_SERVICE_SUITE)

    # test_new_mail_service_goto_menu_wizard_page
    def complete_connect_new_service(self, page):
        mail_to_connect = self.params_dictionary.get("ACRONIS_GMAIL_CONFIGURATION_MAIL")
        my_complete_gmail_configuration_service_connection = CompleteGmailConfigurationPage(page)
        my_complete_gmail_configuration_service_connection.set_gmail_configuration_mail(mail_to_connect)
        my_complete_gmail_configuration_service_connection.click_next_button_enable("G-Suite")

    def test_new_mail_service_add_domain(self, page, params_dictionary):
        my_add_domain_page = NewServiceWizardAddDomain(page)
        # verify we got to set_scanned_mail page
        assert my_add_domain_page.get_add_domain_label_text() == "Domains"
        if self.is_accounts:
            domain_to_add = params_dictionary.get("ACRONIS_DOMAIN_GMAIL2")
            my_add_domain_page.click_accounts()
        else:
            if self.is_acronis:
                domain_to_add = params_dictionary.get("XRAY_DOMAIN_GMAIL")
            else:
                domain_to_add = params_dictionary.get("ACRONIS_DOMAIN_GMAIL1")

        my_add_domain_page.set_host(domain_to_add)
        my_add_domain_page.click_find_domain_smtp_server()
        if self.is_acronis:
            assert my_add_domain_page.set_user_licenses_per_domain(
                self.user_licenses_per_domain) == self.user_licenses_per_domain, "User licenses seats are<>" \
                                                                                 + str(self.user_licenses_per_domain)

        my_add_domain_page.click_next_button()

    def test_new_mail_service_add_text_records(self, page):
        my_verrify_added_domain = verify_domain(page)
        assert my_verrify_added_domain.get_add_text_records_text() == "Add TXT Records"
        my_verrify_added_domain.click_next_button()

    def test_new_mail_service_view_status(self, page):
        my_view_status = view_status(page)
        assert my_view_status.get_allmost_done_text() == "Almost Done!"
        my_view_status.click_view_status_button()
        my_view_status.verify_url(self.base_url + 'settings/domains/')

    def assert_and_report_assertions_of_license_seats(self, organization_details_before):
        acronis_assertions.assert_and_report_assertions_of_license_seats(organization_details_before
                                                                         , self.user_licenses_per_domain
                                                                         , self.acronis_organization_id
                                                                         , self.acronis_token_value)

    def reset_billing_method_and_verify_reset(self, set_billing_method):
        SetupTearDownGuiOperations.reset_billing_method(self.acronis_organization_id
                                                        , self.acronis_token_value
                                                        , set_billing_method)
        jsonBillingStatus = SetupTearDownGuiOperations.get_billing_status(self.acronis_organization_id,
                                                                          self.acronis_token_value)
        if set_billing_method:
            assert jsonBillingStatus["force_use_seats_amount_for_billing"]
        else:
            assert not jsonBillingStatus["force_use_seats_amount_for_billing"]
