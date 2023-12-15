# Todo List

### Code
- [x] Implement is_read retrieval in get_mails service and add this attribute to the email data class
- [x] Create management service for each provider to handle delete/read/unread/
- [ ] Implement asynchronous email retrieval in the background
- [x] Implement logging (remove all print statements ,add to logging window)
- [x] Clean up code (email_util, main_window)
- [/] Perhaps make dedicated pyqt signal hub thing instead of having it all connected to the main window, such that it only need to handle ui stuff
- [x] Create seperate search services for each client type
- [x] Retrieve date and time from gmail

### Attachments
- [x] Preview PDFs
- [ ] View embedded videos
- [x] Images (png, jpg, gif,)
- [x] Sound (mp3, wav)

### GUI
- [x] Email management
- [ ] Folder management
- [x] Dark mode styling (qss file)
- [x] Split styling file into different files for each part of app
- [ ] Pop up info windows (waiting for emails, email sent, email deleted, etc)
- [ ] Windows notifications
- [ ] Improve GUI (make it not look terrible)

### Email management
- [x] Outlook search function
- [ ] Email sorting
- [ ] Spamfilter
- [x] Give email view area its own folder and split into multiple files (email_view_area, web_engine, ToolBarMenu, and one other ive forgotton)
- [ ] Implement settings in settings window

### Testing
- [ ] ...

# Known bugs
- Date and Time for sent and recieved emails dont match (time zones problem i think)
- Recepients field when opening (or saving) drafts (only outlook i think)
- Gmail only retrieves one attachment sometimes
- Cant zoom in pdf viewer (and throws weird js errors)
- Attachment preview for videos isnt working

# Requirements
- google-auth-oauthlib
- google-api-python-client
- msal
- Flask
- PyQt5
- PyQtWebEngine
- scikit-learn
- joblib

### Package Installation
```
pip install google-auth-oauthlib google-api-python-client msal Flask PyQt5 PyQtWebEngine bs4 keyring cryptography scikit-learn joblib
```

# Test Emails
### Outlook
- Mail: dacasoftdev_test@hotmail.com
- Kode: DACAtest
### Gmail
- Mail: dacasoftdev.test@gmail.com
- Kode: DACAtest
