from edc_navbar import NavbarItem, site_navbars, Navbar

edc_calender = Navbar(name='edc_calender')

edc_calender.append_item(
    NavbarItem(name='edc_calender',
               label='EDC CALENDER',
               fa_icon='fa-cogs',
               url_name='home_url'))


site_navbars.register(edc_calender)
