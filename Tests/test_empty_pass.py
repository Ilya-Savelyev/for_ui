from Pages.pages import LoginPage, InventoryPage


def test_auth(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('')
    auth_page.login_button_click()
    auth_page.check_empty_pass()

    # assert InventoryPage(driver).check_inventory_page_open()

