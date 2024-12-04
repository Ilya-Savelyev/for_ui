from Pages.pages import LoginPage, InventoryPage


def test_auth(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('ololololo')
    auth_page.login_button_click()
    auth_page.check_error()

    # assert InventoryPage(driver).check_inventory_page_open()

