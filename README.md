# ipa-filepicker-patcher

**ipa-filepicker-patcher** is a Windows-only command-line tool that automates the process of patching `.ipa` files with a custom certificate and provisioning profile. This tool helps developers and testers quickly sign and modify iOS applications, ensuring that the application identifier (Bundle ID) is updated and the app is ready for installation on a device.

### Features
- Patches `.ipa` files by replacing the application identifier to fix permission issues.
---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/wwyssbb/ipa-filepicker-patcher.git
   cd ipa-filepicker-patcher
   ```
2. Install the zsign:
   
  Download the zsign.exe from its official repository: [zsign](https://github.com/zhlynn/zsign) on GitHub.
  After downloading zsign.exe, place it inside the bin\ folder.

3. Make sure you have Python installed on your system.

## Usage
```bash
python ipa_filepicker_patcher.py -c <certificate(.p12)> -m <mobileprovision> -p <certificate_password> -i <ipa_file>
```
