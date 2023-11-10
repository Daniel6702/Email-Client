# Todo List
- [x] Implement is_read retrieval in get_mails service and add this attribute to the email data class (without breaking everything)
- [x] Create management service for each provider to handle delete/read/unread/
- [ ] Implement asynchronous email retrieval in the background
- [ ] Implement logging (remove all print statements throught out the code and add them to some kind of logging service, perhabs visible in seperate window)
- [ ] Implement settings in settings window
- [ ] Preview attachments (80% DONE, video not working)
- [ ] GUI for email management (delete mail, move email, create folder, delete folder, edit folder) (50%)
- [ ] Dark mode styling (qss file)
- [ ] Split styling file into different files for each part of app
- [ ] Outlook search function
- [ ] Email sorting
- [ ] Spamfilter
- [ ] Pop up info windows (waiting for emails, email sent, email deleted, etc)
- [ ] Windows notifications
- [ ] Clean up (email_util, main_window)
- [ ] Give email view area its own folder and split into multiple files (email_view_area, web_engine, ToolBarMenu, and one other ive forgotton) DONE
- [ ] Perhaps make dedicated pyqt signal hub thing instead of having it all connected to the main window, such that it only need to handle ui stuff
- [ ] Improve GUI (make it not look terrible)

# Known bugs
- Date and Time for sent and recieved emails dont match (time zones problem i think)
- recepients field when opening (or saving) drafts (only outlook i think)
- gmail only retrieves one attachment sometimes
- cant zoom in pdf viewer (and throws weird js errors)
- attachment preview for videos isnt working

# Requirements
- google-auth-oauthlib
- google-api-python-client
- msal
- Flask
- PyQt5
- PyQtWebEngine

## Package Installation
```
pip install google-auth-oauthlib google-api-python-client msal Flask PyQt5 PyQtWebEngine bs4 keyring cryptography
```

# Test Emails
## Outlook
- Mail: dacasoftdev_test@hotmail.com
- Kode: DACAtest
## Gmail
- Mail: dacasoftdev.test@gmail.com
- Kode: DACAtest
