def phone_lookup():
    """Function to parse, format, and analyze phone numbers with country auto-fallback."""
    clear_screen()
    display_banner()
    print("[+] --- ADVANCED PHONE LOOKUP OPTION --- [+]\n")
    
    raw_input = input("Enter phone number to look up (e.g., +34600123456 or 600123456): ").strip()
    
    # Remove common formatting characters to clean the input
    cleaned_input = re.sub(r'[\s\-\(\)]', '', raw_input)
    
    default_region = None
    # If the number doesn't start with '+', ask for the country code to avoid formatting errors
    if not cleaned_input.startswith('+'):
        print("\n[*] No country code prefix (+) detected.")
        default_region = input("Enter 2-letter Country Code (e.g., ES for Spain, US, GB, IN): ").strip().upper()
        if not default_region:
            default_region = None

    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(cleaned_input, default_region)
        
        # Validation checks
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        print("\n---------------- Phone Information ----------------")
        print(f"Parsed Number (E.164): {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"National Format      : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        print(f"International Format : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"RFC3966 Telecom URL  : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.RFC3966)}")
        print(f"Country Code Prefix  : +{parsed_number.country_code}")
        print(f"National Destination : {parsed_number.national_number}")
        print(f"Structural Validation: {'VALID' if is_valid else 'INVALID'}")
        print(f"Is Possible Number   : {'YES' if is_possible else 'NO'}")
        
        # Geolocation / Location Details
        # "en" requests the description in English
        region_name = geocoder.description_for_number(parsed_number, "en")
        country_name = geocoder.country_name_for_number(parsed_number, "en")
        
        print("\n---------------- Geographic Details ----------------")
        print(f"Country of Origin    : {country_name if country_name else 'Unknown'}")
        print(f"Specific Location/City: {region_name if region_name else 'Unknown/Not Specified'}")
        
        # Carrier / Network Details
        carrier_name = carrier.name_for_number(parsed_number, "en")
        print("\n---------------- Carrier Details ----------------")
        print(f"Carrier/Provider     : {carrier_name if carrier_name else 'Unknown (or Landline/VoIP)'}")
        
        # Timezone Details
        timezones = phone_timezone.time_zones_for_number(parsed_number)
        print("\n---------------- Network Timezones ----------------")
        print(f"Timezones Associated : {', '.join(timezones) if timezones else 'Unknown'}")
        
        # Line Type Classification
        number_type = phonenumbers.number_type(parsed_number)
        type_mapping = {
            0: "Fixed Line (Landline)",
            1: "Mobile",
            2: "Fixed Line or Mobile (Shared/Hybrid)",
            3: "Toll Free (No Charge to Caller)",
            4: "Premium Rate (Paid Service)",
            5: "Shared Cost",
            6: "VoIP (Voice over IP / Internet Phone)",
            7: "Personal Number",
            8: "Pager",
            9: "Universal Access Number (UAN)",
            10: "Voice Mail Service",
            -1: "Unknown / Unclassified"
        }
        print("\n---------------- Line Specification ----------------")
        print(f"Line Type Category   : {type_mapping.get(number_type, 'Unknown')}")
        
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"\n[-] Parsing Failed: {e}")
        print("[*] Please ensure you enter the number correctly or specify the country code when prompted.")
        
    input("\nPress Enter to return to the main menu...")
