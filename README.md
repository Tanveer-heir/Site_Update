# 🌐 Website Change Monitor

A robust Python tool for monitoring webpages for changes.  
When a change is detected, logs the event, saves a snapshot of the page, and can send an email notification.

---

## 🚀 Features

- Detects updates to any webpage via hash comparison
- Supports multiple hash algorithms (`md5`, `sha1`, `sha256`, etc.)
- Timestamped **logging** of all checks and changes
- **Snapshot** saving of changed HTML content
- Optional **email notifications** via Gmail
- Command-line interface – easy to automate & schedule
- Graceful exit and final summary reporting

---

### All Command-Line Arguments

| Argument      | Required | Description                                  | Example Value              |
|---------------|----------|----------------------------------------------|----------------------------|
| `--url`       | Yes      | Website to monitor                           | https://example.com        |
| `--interval`  | No       | Check interval (seconds, default=60)         | 120                        |
| `--log`       | No       | Log file path (default: monitor.log)         | my_monitor.log             |
| `--algo`      | No       | Hash algorithm (`md5`, `sha1`, etc.)         | sha256                     |
| `--email`     | No       | Sender Gmail for notifications               | your.email@gmail.com       |
| `--password`  | No       | Sender Gmail App Password                    | your_app_password          |
| `--to`        | No       | Recipient email for notifications            | recipient@gmail.com        |
| `--snapshots` | No       | Directory for saved HTML snapshots           | snapshots                  |

### Example

Monitor a site with custom interval and hashing

---

## 📂 Output

- **Log file** records all activity.
- **Snapshots folder** stores .html pages when changes are detected.

---

## 🛠️ Notes

- For email notifications, you must use a Gmail app password (not your regular password, especially if you use 2FA).
- Interrupt with `Ctrl+C` to stop and see a summary.
- Works on Windows, macOS, Linux.

---

## 📝 License

MIT

---

*Made by Tanveer Singh, open for improvements and suggestions!*


