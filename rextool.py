import os
import sys
import smtplib
import getpass
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import external libraries and handle missing dependencies gracefully
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone as phone_timezone
except ImportError:
    print("[-] Error: 'phonenumbers' library is missing.")
    print("[*] Please install it using: pip install phonenumbers")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[-] Error: 'requests' library is missing.")
    print("[*] Please install it using: pip install requests")
    sys.exit(1)

try:
    import dns.resolver
except ImportError:
    print("[-] Error: 'dnspython' library is missing.")
    print("[*] Please install it using: pip install dnspython")
    sys.exit(1)


def clear_screen():
    """Clears the terminal screen in Linux."""
    os.system('clear')


def display_banner():
    """Displays the REX TOOL ASCII art."""
    banner = """
██████╗ ███████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔════╝╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝█████╗   ╚███╔╝        ██║   ██║   ██║██║   ██║██║     
██╔══██╗██╔══╝   ██╔██╗        ██║   ██║   ██║██║   ██║██║     
██║  ██║███████╗██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    print(banner)
    print("===============================================================")
    print("                      System Utilities Menu                    ")
    print("===============================================================\n")


def email_sender():
    """Function to send emails via SMTP."""
    clear_screen()
    display_banner()
    print("[+] --- EMAIL SENDER OPTION --- [+]\n")

    print("Select SMTP Provider:")
    print("1. Gmail (smtp.gmail.com)")
    print("2. Outlook/Hotmail (smtp.office365.com)")
    print("3. Yahoo (smtp.mail.yahoo.com)")
    print("4. Custom SMTP")
    
    provider_choice = input("\nChoose an option [1-4]: ").strip()
    
    if provider_choice == '1':
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif provider_choice == '2':
        smtp_server = "smtp.office365.com"
        smtp_port = 587
    elif provider_choice == '3':
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = 587
    elif provider_choice == '4':
        smtp_server = input("Enter SMTP Server Address: ").strip()
        try:
            smtp_port = int(input("Enter SMTP Port (usually 587 or 465): ").strip())
        except ValueError:
            print("Invalid port number. Defaulting to 587.")
            smtp_port = 587
    else:
        print("Invalid choice. Returning to menu.")
        input("\nPress Enter to return...")
        return

    sender_email = input("\nEnter your email address: ").strip()
    sender_password = getpass.getpass("Enter your password (or App Password): ")
    
    recipient_email = input("Enter recipient email address: ").strip()
    subject = input("Enter email subject: ").strip()
    message_body = input("Enter message content: ")
    
    try:
        count = int(input("How many times do you want to send this email?: ").strip())
        if count <= 0:
            print("Count must be greater than 0.")
            input("\nPress Enter to return...")
            return
    except ValueError:
        print("Invalid number entered. Aborting.")
        input("\nPress Enter to return...")
        return

    print("\n[+] Attempting to send email(s)...")
    
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            
        server.login(sender_email, sender_password)
        
        for i in range(1, count + 1):
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"{subject} (Copy #{i})" if count > 1 else subject
            msg.attach(MIMEText(message_body, 'plain'))
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"[{i}/{count}] Email sent successfully to {recipient_email}")
            
        server.quit()
        print("\n[+] All tasks completed.")
        
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")
        print("Verify your credentials, network connection, and SMTP settings.")
        
    input("\nPress Enter to return to the main menu...")


def phone_lookup():
    """Function to parse and analyze phone numbers."""
    clear_screen()
    display_banner()
    print("[+] --- PHONE LOOKUP OPTION --- [+]\n")
    print("Note: Always include the country code (e.g., +14155552671)\n")
    
    raw_number = input("Enter phone number to look up: ").strip()
    
    try:
        parsed_number = phonenumbers.parse(raw_number)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        print("\n---------------- Results ----------------")
        print(f"Input Number        : {raw_number}")
        print(f"Formatted National  : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        print(f"Formatted Internat. : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"Country Code        : {parsed_number.country_code}")
        print(f"National Number     : {parsed_number.national_number}")
        print(f"Is Possible Number  : {is_possible}")
        print(f"Is Valid Number     : {is_valid}")
        
        if is_valid:
            region = geocoder.description_for_number(parsed_number, "en")
            print(f"Location/Region     : {region if region else 'Unknown'}")
            
            carrier_name = carrier.name_for_number(parsed_number, "en")
            print(f"Carrier/Provider    : {carrier_name if carrier_name else 'Unknown or Landline'}")
            
            timezones = phone_timezone.time_zones_for_number(parsed_number)
            print(f"Timezone(s)         : {', '.join(timezones)}")
            
            number_type = phonenumbers.number_type(parsed_number)
            type_mapping = {
                0: "Fixed Line", 1: "Mobile", 2: "Fixed Line or Mobile",
                3: "Toll Free", 4: "Premium Rate", 5: "Shared Cost",
                6: "VoIP", 7: "Personal Number", 8: "Pager",
                9: "Universal Access Number", 10: "Voice Mail", -1: "Unknown"
            }
            print(f"Line Type           : {type_mapping.get(number_type, 'Unknown')}")
        else:
            print("\n[-] Invalid phone number format. Please check the country code.")
            
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"\n[-] Error parsing number: {e}")
        print("[*] Make sure to start the number with '+' followed by the country code.")
        
    input("\nPress Enter to return to the main menu...")


def ip_lookup():
    """Function to perform geolocation lookup on an IP address."""
    clear_screen()
    display_banner()
    print("[+] --- IP LOOKUP OPTION --- [+]\n")
    
    target_ip = input("Enter IP Address (leave blank to lookup your own IP): ").strip()
    
    print("\n[+] Fetching IP information...")
    try:
        # Requesting data from free public geolocation API
        api_url = f"http://ip-api.com/json/{target_ip}"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data.get("status") == "success":
            print("\n---------------- Results ----------------")
            print(f"IP Address    : {data.get('query')}")
            print(f"Country       : {data.get('country')} ({data.get('countryCode')})")
            print(f"Region/State  : {data.get('regionName')}")
            print(f"City          : {data.get('city')}")
            print(f"ZIP Code      : {data.get('zip')}")
            print(f"Coordinates   : Lat: {data.get('lat')}, Lon: {data.get('lon')}")
            print(f"Timezone      : {data.get('timezone')}")
            print(f"ISP Provider  : {data.get('isp')}")
            print(f"Organization  : {data.get('org')}")
            print(f"ASN           : {data.get('as')}")
        else:
            print(f"\n[-] Failed to resolve IP. Reason: {data.get('message', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Connection error: {e}")
        
    input("\nPress Enter to return to the main menu...")


def email_lookup():
    """Function to perform syntax validation and MX record checks on an email."""
    clear_screen()
    display_banner()
    print("[+] --- EMAIL LOOKUP OPTION --- [+]\n")
    
    target_email = input("Enter email address to check: ").strip()
    
    # Syntax Validation via Regular Expression
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    print("\n---------------- Results ----------------")
    print(f"Target Email    : {target_email}")
    
    if not re.match(email_regex, target_email):
        print("Syntax Status   : INVALID (Failed basic email formatting rules)")
        input("\nPress Enter to return to the main menu...")
        return
    else:
        print("Syntax Status   : VALID (Well-formed email structure)")
        
    # Extract domain for MX record checks
    domain = target_email.split('@')[-1]
    print(f"Target Domain   : {domain}")
    
    print("\n[+] Querying public DNS records for MX (Mail Servers)...")
    try:
        # Perform DNS lookup for MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f"Domain Status   : ACTIVE (Has functioning mail servers)\n")
        print("Identified Mail Servers (MX):")
        for record in mx_records:
            print(f"  - {record.exchange.to_text().strip('.')} (Priority: {record.preference})")
            
    except dns.resolver.NoAnswer:
        print("\nDomain Status   : INACTIVE (No MX records found. This domain cannot receive emails.)")
    except dns.resolver.NXDOMAIN:
        print("\nDomain Status   : NOT FOUND (The domain name does not exist.)")
    except Exception as e:
        print(f"\n[-] DNS Lookup failed: {e}")
        
    input("\nPress Enter to return to the main menu...")


def main_menu():
    while True:
        clear_screen()
        display_banner()
        print("1. Email Sender")
        print("2. Phone Lookup")
        print("3. IP Lookup")
        print("4. Email Lookup")
        print("5. Exit")
        
        choice = input("\nSelect an option [1-5]: ").strip()
        
        if choice == '1':
            email_sender()
        elif choice == '2':
            phone_lookup()
        elif choice == '3':
            ip_lookup()
        elif choice == '4':
            email_lookup()
        elif choice == '5':
            print("\nExiting REX TOOL. Goodbye.")
            sys.exit()
        else:
            print("\nInvalid choice. Please choose between 1 and 5.")
            input("\nPress Enter to try again...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nSession terminated by user.")
        sys.exit()
