   ########################################################

        for index, row in df_em_app.iterrows():
            if '@' in row['EmailAddress'] and row['EmailAddress'].strip() not in ['-', '']:
                continue
            else:
                messages.error(request, "Column Contain Incorrect Values !")
                return redirect('email_home')

        data1.email_user = uploaded_user

        df =pd.read_csv(dv_final_file_1)
        
        #################### irfan changes #####################################
        # Define the columns and their default values
        columns_with_defaults = {
            'Email_Veri_ID': "Not_An_ID",
            'Email_Veri_Status': "-"
        }

        # Check and create the columns if they don't exist
        for column, default_value in columns_with_defaults.items():
            if column not in df.columns:
                df[column] = default_value
        ############ irfan changes end
        today_datetime = datetime.today()
        
        file_count=len(df_em_app)
        Email_Count=data2.Email_Count
        updated_Email_Count=Email_Count-file_count
        data2.Email_Count=updated_Email_Count
        data2.save()

        df_em_app['Profileurl'] = df_em_app['Profileurl'].str.rstrip('/')
        df_em_app['Profileurl'] = df_em_app['Profileurl'].str.lower()

        for index, row in df_em_app.iterrows():
            my_model_obj = Email_append_uploaded_data(
                Li_profile_url=row['Profileurl'],
                company_name=row['Organization1'],
                email_address=row['EmailAddress'],
                created_at=today_datetime,
            )
            my_model_obj.save()
 


        for index, row in df.iterrows():
            row['Profileurl'] = row['Profileurl'].rstrip('/')
            row['Profileurl'] = row['Profileurl'].lower()
            profileurl = row['Profileurl']
            matching_row = df_em_app[df_em_app['Profileurl'] == profileurl]
            if not matching_row.empty:
                df.at[index, 'EmailAddress'] = matching_row['EmailAddress'].iloc[0]
                df.at[index, 'Email_Domain Error'] = '-'
                df.at[index, 'File_Save_Date'] = today_datetime.date()
                df_em_app.at[matching_row.index[0], 'Email_Verification_Status'] = row['Email_Verification_Status']
                df_em_app.at[matching_row.index[0], 'EV'] = row['EV']
                # df_em_app.at[matching_row.index[0], 'EV'] = 'Fresh Email Created'

            bot_reasons = row['Bot_Reason'].split(',')
            if bot_reasons == ['Email Format Invalid']:
                df.at[index, 'Bot_Reason'] = 'Qualified'
            else:
                bot_reasons = [reason for reason in bot_reasons if reason != 'Email Format Invalid']
                df.at[index, 'Bot_Reason'] = ','.join(bot_reasons)


        #############################################################

        

        if (df_em_app['EV'] == "1").any():
            print("No")
            ################## Change Status ########################
            df['EV'] = df['EV'].astype(str)
            disqualified_mask = (df['Email_Verification_Status'] == "Nondeliverable") & (df["EV"] == '1')
            
            df.loc[disqualified_mask, 'EV'] = np.where(
                (df.loc[disqualified_mask, 'EV'] == '1') & (df.loc[disqualified_mask, 'Email_Append_ID'] == str(data_id)),
                '2',
                df.loc[disqualified_mask, 'EV']
            )

            df_em_app['EV'] = np.where(
                df_em_app['EV'] == '1',
                '2',
                df_em_app['EV']
            )
            
            email_ver_df = df_em_app[(df_em_app['Email_Verification_Status'] == "Nondeliverable") & (df_em_app["EV"] == '2')]

            # columns_to_fetch = ['CampaignName','Profileurl','Domain','EmailAddress','Firstname','Lastname','TelephoneNumber','Organization1','OrganizationTitle1','Country','Email_Veri_ID']
            # email_ver_df = email_ver_df[columns_to_fetch]
            # email_ver_df = email_ver_df.rename(columns={'CampaignName': 'Campaign ID', 'Profileurl': 'Profile Link', 'EmailAddress': 'Email ID','Firstname': 'First Name','Lastname': 'Last Name','TelephoneNumber':'Phone number','Organization1':'Company Name','OrganizationTitle1':'Job Title'})
            # email_ver_df["WP"] = "-"
            # email_ver_df['Email_Status']= '-'
            # email_ver_df['SG_Status']= '-'

            Email_verified_count=len(email_ver_df.index)
            print(Email_verified_count)
            data1.post_append_count = Email_verified_count
            data1.save()

            ##File uploaded mail  count Email_verified_count
            tables_side_by_side = (
                    "<div class='flex-container col-sm-12'>"
                    "<div style='display: flex; justify-content: space-between;'>"
                    "<div class='subsection-container'>"
                    "<br>"
                    "<div class='col-md-6'>"
                    "<table border='1' style='border-collapse: collapse; width: 30%;'>"
                    "<tr style='background-color: lightblue;'>"
                    "<th style='padding: 8px;' colspan='2'>Email Append Stats:</th></tr>"
                    # "<th style='padding: 8px; background-color: lightblue;'>Fields</th><th style='padding: 8px; background-color: lightblue;'>Count</th></tr>"
                    f"<tr><td style='padding: 8px;'>Count For Email Verification</td><td style='padding: 8px;'>{Email_verified_count}</td></tr>"
                    f"<tr><td style='padding: 8px; background-color: lightblue; font-weight: bold;'>Total</td><td style='padding: 8px; background-color: lightblue; font-weight: bold;'>{Email_verified_count}</td></tr>"
                    "</table>"
                    "</div>"
                    "</div>"
                    "</div>"
                    "</div>"
                )

            main_message1 = f'Hi Team,'
            main_message2 = f'Please find below the completed count for Email Verification after the Email Append process for the campaign {campaign_code}, which was sent by Email Verification.'
            signature = f'<h3 style="font-weight: bold;">Thanks & Regards,<br>Fetchmatica Team</h3>'

            # Create the EmailMessage instance for sending the email
            email = EmailMultiAlternatives(
                f'Email_Verification_Required {campaign_code} - FetchMatica.',
                'New BCL request for DV process completed',
                'fetchmatica@facileserv.com',
                ['databots_team@facileserv.com','rsj@facileserv.com','Pradip.Koparde@facileserv.com','ashwini.wakhare@facileserv.com','campaign_delivery@facileserv.in','delivery@facileserv.in','qateam@facileserv.in','em@facileserv.in','libtteam@facileserv.in','opsappendrequest@facileserv.in','opsmgmt@facileserv.in'],
            )
            # Add HTML content to the email
            email.attach_alternative(f'{main_message1}<br>{main_message2}<br><br>{tables_side_by_side}<br><br><br>{signature}', "text/html")

            # Send the email
            email.send()

            if not email_ver_df.empty:
                data19 = Send_Data5.objects.get(id=send_data_id)
                new2 = Email_verification(
                    send_data = data19,
                    pre_verification_count = Email_verified_count,
                    status = "Email Append EV"
                )
                new2.save()
                email_ver_id = new2.pk
                
                
                df_email_ver_indexed = email_ver_df.set_index('Profileurl')
                df['Profileurl1'] = df['Profileurl'].str.rstrip('/')
                df['Profileurl1'] = df['Profileurl1'].str.lower()
                
                df.loc[df['Profileurl1'].isin(df_email_ver_indexed.index), 'Email_Veri_ID'] = str(email_ver_id)
                df = df.drop(['Profileurl1'], axis=1)
                # campaign_code = data2.campaign_code
                # data4 = Email_verification.objects.get(id=email_ver_id)
                # print(' email verified file saving process start')
                # buffer = io.StringIO()
                # email_ver_df.to_csv(buffer, index=False)
                # csv_data = buffer.getvalue().encode('utf-8')
                # # data2 = Send_Data5.objects.get(id=id1)
                # data4.download_email_verified_file.save(f'Email_Verification_Data_{campaign_code}.csv', ContentFile(csv_data), save=True)
                # print('email verified file saving process done')

        #####################################################
        if (df_em_app['EV'] == "Fresh Email Created" ).any():
            print("Fresh Email Done")
            df['EV'] = df['EV'].astype(str)
            df['EV'] = np.where(
                (df['EV'] == 'Fresh Email Created') & (df['Email_Append_ID'] == str(data_id)),
                'Fresh Email Done',
                df['EV']
            )
            df_em_app['EV'] = np.where(
                df_em_app['EV'] == 'Fresh Email Created',
                'Fresh Email Done',
                df_em_app['EV']
            )
            ############ irfan changes
            
            email_ver_df2 = df_em_app[(df_em_app["EV"] == 'Fresh Email Done')]
   
            Email_verified_count=len(email_ver_df2.index)
            print(Email_verified_count)
            data1.post_append_count = Email_verified_count
            data1.save()
            if not email_ver_df2.empty:
                print(email_ver_df2.columns)
                data19 = Send_Data5.objects.get(id=send_data_id)
                new5 = Email_verification(
                    send_data = data19,
                    pre_verification_count = Email_verified_count,
                    status = "Email Append EV"
                )
                new5.save()
                email_ver_id = new5.pk
                df_email_ver_indexed1 = email_ver_df2.set_index('Profileurl')
           
                df['Profileurl1'] = df['Profileurl'].str.rstrip('/')
                df['Profileurl1'] = df['Profileurl1'].str.lower()
             
                df.loc[df['Profileurl1'].isin(df_email_ver_indexed1.index), 'Email_Veri_ID'] = str(email_ver_id)
                df = df.drop(['Profileurl1'], axis=1)

                tables_side_by_side = (
                    "<div class='flex-container col-sm-12'>"
                    "<div style='display: flex; justify-content: space-between;'>"
                    "<div class='subsection-container'>"
                    "<br>"
                    "<div class='col-md-6'>"
                    "<table border='1' style='border-collapse: collapse; width: 30%;'>"
                    "<tr style='background-color: lightblue;'>"
                    "<th style='padding: 8px;' colspan='2'>Email Append Stats:</th></tr>"
                    # "<th style='padding: 8px; background-color: lightblue;'>Fields</th><th style='padding: 8px; background-color: lightblue;'>Count</th></tr>"
                    f"<tr><td style='padding: 8px;'>Count For Email Verification</td><td style='padding: 8px;'>{Email_verified_count}</td></tr>"
                    f"<tr><td style='padding: 8px; background-color: lightblue; font-weight: bold;'>Total</td><td style='padding: 8px; background-color: lightblue; font-weight: bold;'>{Email_verified_count}</td></tr>"
                    "</table>"
                    "</div>"
                    "</div>"
                    "</div>"
                    "</div>"
                )

                main_message1 = f'Hi Team,'
                main_message2 = f'Please find below the completed count for Email Verification after the Email Append process for the campaign {campaign_code}, which was sent by DV.'
                signature = f'<h3 style="font-weight: bold;">Thanks & Regards,<br>Fetchmatica Team</h3>'

            # Create the EmailMessage instance for sending the email
                email = EmailMultiAlternatives(
                    f'Email_Verification_Required {campaign_code} - FetchMatica .',
                    'New BCL request for DV process completed',
                    'fetchmatica@facileserv.com',
                    ['databots_team@facileserv.com','rsj@facileserv.com','Pradip.Koparde@facileserv.com','ashwini.wakhare@facileserv.com','campaign_delivery@facileserv.in','delivery@facileserv.in','qateam@facileserv.in','em@facileserv.in','libtteam@facileserv.in','opsappendrequest@facileserv.in','opsmgmt@facileserv.in'],
                )
                # Add HTML content to the email
                email.attach_alternative(f'{main_message1}<br>{main_message2}<br><br>{tables_side_by_side}<br><br><br>{signature}', "text/html")

                # Send the email
                email.send()

        ####################################################################


        
        Quali_Count = 0
        Phone_Count = 0
        Industry_Count = 0
        Title_Count = 0
        Email_Count = 0
        Address_Count = 0
        Disqualified_Count = 0
        All_Append_Count = 0
        Dead_Contact_Error = 0
        Name_recheck_Count = 0
        Job_Title_DisQua_count = 0
        WO_HO_Location_count = 0
        Job_Contract_count = 0
        Negetive_Keyword_count = 0
        Job_Level_Not_Matched_count = 0
        AC_not_matched_count=0
        Same_prospect_matched_count=0
        Employee_size_disquali_count = 0
        Address_Append_disquali_count = 0
        Name_recheck_disquali_count = 0
        Phone_number_disquali_count = 0
        for index,row in df.iterrows():
            if row['Bot_Status'] == 'Qualified' and row['Bot_Reason'] == 'Qualified':
                Quali_Count += 1
            if row['Bot_Status'] == 'Qualified' and row['Bot_Reason'] != 'Qualified':
                All_Append_Count += 1
            if row['Bot_Status'] == 'Disqualified':
                Disqualified_Count += 1
            if row['Bot_Status'] == 'Qualified' and 'Phone Number Need Append' in row['Bot_Reason']:
                Phone_Count += 1
            if row['Bot_Status'] == 'Qualified' and 'Title Need Append' in row['Bot_Reason']:
                Title_Count += 1
            if row['Bot_Status'] == 'Qualified' and 'Industry_Type Need Append' in row['Bot_Reason']:
                Industry_Count += 1
            if row['Bot_Status'] == 'Qualified' and 'Email Format Invalid' in row['Bot_Reason']:

                Email_Count += 1
            if row['Bot_Status'] == 'Qualified' and 'Name Need To Recheck' in row['Bot_Reason']:
                Name_recheck_Count += 1
            if row['Bot_Status'] == 'Qualified' and any(append_condition in row['Bot_Reason'] for append_condition in ['State Append', 'City Append', 'Address Append', 'Zip_Code Append']):
                Address_Count += 1
            ############## Disqualified Count #################
            if row['Bot_Status'] == 'Disqualified' and 'Dead_Contact' in row['Bot_Reason']:
                Dead_Contact_Error += 1
            elif row['Bot_Status'] == 'Disqualified' and 'Negetive Keyword' in row['Bot_Reason']:
                Negetive_Keyword_count += 1
            elif row['Bot_Status'] == 'Disqualified' and 'Job_Contract' in row['Bot_Reason']:
                Job_Contract_count += 1
            elif row['Bot_Status'] == 'Disqualified' and 'Job_Title' in row['Bot_Reason']:
                Job_Title_DisQua_count += 1
            elif row['Bot_Status'] == 'Disqualified' and 'Account List Not Matched' in row['Bot_Reason']:
                AC_not_matched_count += 1
            elif row['Bot_Status'] == 'Disqualified' and 'Same Prospect' in row['Bot_Reason']:
                Same_prospect_matched_count += 1
            
            elif row['Bot_Status'] == 'Disqualified' and 'WO/HO Location' in row['Bot_Reason']:
                WO_HO_Location_count += 1
            
            elif row['Bot_Status'] == 'Disqualified' and 'Employee_Size Not Matched' in row['Bot_Reason']:
                Employee_size_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Employee_Size Need Append' in row['Bot_Reason']:
                Employee_size_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Zip_Code Append' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Phone Number Need Append,' in row['Bot_Reason']:
                Phone_number_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'State Append' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'City Append' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Address Append' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Email Format Invalid' in row['Bot_Reason']:
                WO_HO_Location_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Invalid Geo' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Other Country' in row['Bot_Reason']:
                Address_Append_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Dnc_phone' in row['Bot_Reason']:
                Phone_number_disquali_count += 1
                
            elif row['Bot_Status'] == 'Disqualified' and 'Name Need To Recheck' in row['Bot_Reason']:
                Name_recheck_disquali_count += 1
        

        data2.DV_Qualified_data = Quali_Count
        data2.DV_Qualified_Append_data = All_Append_Count
        data2.DV_Disqualified_data = Disqualified_Count
        data2.Phone_append_Count = Phone_Count
        data2.Industry_append_Count = Industry_Count
        data2.Title_append_Count = Title_Count
        data2.Email_Count = Email_Count
        data2.Address_append_Count = Address_Count
        data2.Name_Rechecked_Count = Name_recheck_Count
        data2.Dead_Contact_Count = Dead_Contact_Error
        data2.Job_function_DisQua_count = Job_Title_DisQua_count
        data2.WO_HO_Location_count = WO_HO_Location_count
        data2.Job_Contract_count = Job_Contract_count
        data2.Negetive_Keyword_count = Negetive_Keyword_count
        data2.Job_Level_Not_Matched_count = Job_Level_Not_Matched_count
        data2.AC_not_matched_count = AC_not_matched_count
        data2.Same_Prospect_disqualified_count = Same_prospect_matched_count
        data2.Employee_size_disquali_count = Employee_size_disquali_count
        data2.Address_Append_disquali_count =Address_Append_disquali_count 
        data2.Name_recheck_disquali_count = Name_recheck_disquali_count
        data2.Phone_number_disquali_count = Phone_number_disquali_count
        data2.save()

        data3 = Send_Data5.objects.get(id=send_data_id)
        ################################################################
        print('file saving process start')
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        csv_data = buffer.getvalue().encode('utf-8')
        # data2 = Send_Data5.objects.get(id=id1)
        campaign_code = data3.campaign_code
        data3.dv_final_file.save(f'DV_final_file_{campaign_code}.csv', ContentFile(csv_data), save=True)
        print('file saving process done')
        ################################################################
        messages.success(request,'File is uploaded!! ')
        return redirect('email_home')
    return render(request, 'Email_Append/home.html')