import streamlit as st
import helper


uploaded_file = st.sidebar.file_uploader("Choose a file", type="pdf")
balance_sheet, statement_of_operations, statements_of_comprehensive_income, statement_of_cash_flow = helper.process_pdf(uploaded_file)

        
# Start Working on the Balance Sheet Column
        #Rename the column names
if balance_sheet is not None and statements_of_comprehensive_income is not None and statement_of_cash_flow is not None and statement_of_operations is not None:

        balance_sheet.rename(columns={"Unnamed: 0": "December 31, 2023"}, inplace=True)
        balance_sheet.rename(columns={"Unnamed: 2": "December 31, 2022"}, inplace=True)

        #edit the values 
        value_at_1_2 = balance_sheet.iloc[1, 2]
        balance_sheet.iloc[1, 1] = value_at_1_2

        value_at_16_2 = balance_sheet.iloc[16,2]
        balance_sheet.iloc[16,1] = value_at_16_2

        value_at_19_2 = balance_sheet.iloc[19,2]
        balance_sheet.iloc[19,1] = value_at_19_2

        value_at_39_2 = balance_sheet.iloc[39,2]
        balance_sheet.iloc[39,1] = value_at_39_2

        value_at_1_5 = balance_sheet.iloc[1,5]
        balance_sheet.iloc[1,3] = value_at_1_5

        value_at_16_5 = balance_sheet.iloc[16,5]
        balance_sheet.iloc[16,3] = value_at_16_5

        value_at_19_5 = balance_sheet.iloc[19,5]
        balance_sheet.iloc[19,3] = value_at_19_5
        
        value_at_39_5 = balance_sheet.iloc[39,5]
        balance_sheet.iloc[39,3] = value_at_39_5

        #Delete columns
        balance_sheet.drop("Unnamed: 1", axis = 1 , inplace = True)
        balance_sheet.drop("Unnamed: 3", axis = 1 , inplace = True)
        balance_sheet.drop("Unnamed: 4", axis = 1 , inplace = True)

        #Remove Commas from the data set
        balance_sheet['December 31, 2023'] = balance_sheet['December 31, 2023'].str.replace(',', '', regex=False)
        balance_sheet['December 31, 2022'] = balance_sheet['December 31, 2022'].str.replace(',', '', regex=False)

                # Display the selected table
                        #st.write("Balance Sheet:")
                #st.write(balance_sheet)

        #Current assets extract from balance sheet 
        total_assets = balance_sheet.copy()

#         # Remove rows from the current asset data set
        total_assets.drop(0,axis = 0 , inplace = True)
        total_assets.drop(total_assets.index[16:], axis=0, inplace=True)

#         #Resultant show of Current assets
        #st.write("Total Assets: ")
        #st.write(total_assets)

        #Liabilities and Equity extract from balance sheet
        liabilities = balance_sheet.copy()

         # Drop the concatenated row index ranges
        liabilities.drop(liabilities.index[:19], inplace=True)
        liabilities.drop(liabilities.index[11:13], inplace=True)
        liabilities.drop(liabilities.index[9], inplace=True)

        #Rename the column names
        liabilities.rename(columns={"Assets": "Total Liabilities & Equity"}, inplace=True)

        # Reset Index
        liabilities.reset_index(drop=True, inplace=True)

#         #Resultant show of Liabilities
        #st.write("Total Liabilities & Equity: ")
        #st.write(liabilities)
        
# Start Working on the Statement of Operations
        #Rename the column names
        statement_of_operations.rename(columns={"Unnamed: 0": "December 31, 2023"}, inplace=True)
        statement_of_operations.rename(columns={"Unnamed: 2": "December 31, 2022"}, inplace=True)
        statement_of_operations.rename(columns={"Unnamed: 4": "December 31, 2021"}, inplace=True)
        
        #edit the values 
        value_at_0_or_2 = statement_of_operations.iloc[0, 2]
        statement_of_operations.iloc[0, 1] = value_at_0_or_2

        value_at_0_or_5 = statement_of_operations.iloc[0, 5]
        statement_of_operations.iloc[0, 3] = value_at_0_or_5

        value_at_0_or_8 = statement_of_operations.iloc[0, 8]
        statement_of_operations.iloc[0, 5] = value_at_0_or_8

        value_at_28_or_2 = statement_of_operations.iloc[28, 2]
        statement_of_operations.iloc[28, 1] = value_at_28_or_2

        value_at_28_or_5 = statement_of_operations.iloc[28, 5]
        statement_of_operations.iloc[28, 3] = value_at_28_or_5

        value_at_28_or_8 = statement_of_operations.iloc[28, 8]
        statement_of_operations.iloc[28, 5] = value_at_28_or_8

        value_at_31_or_2 = statement_of_operations.iloc[31, 2]
        statement_of_operations.iloc[31, 1] = value_at_31_or_2

        value_at_31_or_5 = statement_of_operations.iloc[31, 5]
        statement_of_operations.iloc[31, 3] = value_at_31_or_5

        value_at_31_or_8 = statement_of_operations.iloc[31, 8]
        statement_of_operations.iloc[31, 5] = value_at_31_or_8

        value_at_32_or_2 = statement_of_operations.iloc[32, 2]
        statement_of_operations.iloc[32, 1] = value_at_32_or_2

        value_at_32_or_5 = statement_of_operations.iloc[32, 5]
        statement_of_operations.iloc[32, 3] = value_at_32_or_5

        value_at_32_or_8 = statement_of_operations.iloc[32, 8]
        statement_of_operations.iloc[32, 5] = value_at_32_or_8

        #Delete columns
        statement_of_operations.drop("Unnamed: 1", axis = 1 , inplace = True)
        statement_of_operations.drop("Unnamed: 3", axis = 1 , inplace = True)
        statement_of_operations.drop("Unnamed: 5", axis = 1 , inplace = True)
        statement_of_operations.drop("Unnamed: 6", axis = 1 , inplace = True)
        statement_of_operations.drop("Unnamed: 7", axis = 1 , inplace = True)

        #Remove Commas from the data set
        statement_of_operations['December 31, 2023'] = statement_of_operations['December 31, 2023'].str.replace(',', '', regex=False)
        statement_of_operations['December 31, 2022'] = statement_of_operations['December 31, 2022'].str.replace(',', '', regex=False)
        statement_of_operations['December 31, 2021'] = statement_of_operations['December 31, 2021'].str.replace(',', '', regex=False)
#show rsults of statement of operations
        #st.write("Statement of Operations:")
#st.wre(statement_of_operations)

#CreateTotal revenue table
        total_revenue = statement_of_operations.copy()
         # Drop the row index ranges
        total_revenue.drop(total_revenue.index[7:], inplace=True)
        total_revenue.drop(total_revenue.index[3], inplace=True)
        # Reset Index
        total_revenue.reset_index(drop=True, inplace=True)
#show esults of 
#st.write("Total Revenue:")     
 #st.write(total_revenue)
        #CreateCost of Revenue table
        total_cost_of_revenue = statement_of_operations.copy()

                # Drop the row index ranges
        total_cost_of_revenue.drop(total_cost_of_revenue.index[14:], inplace=True)
        total_cost_of_revenue.drop(total_cost_of_revenue.index[:8], inplace=True)
        total_cost_of_revenue.drop(total_cost_of_revenue.index[2], inplace=True)

                # Reset Index
        total_cost_of_revenue.reset_index(drop=True, inplace=True)

        #show results of Total cost of Revenue
        #st.write("Total Cost of Revenue:")
        #st.write(total_cost_of_revenue)

#Create Gross Profit (Total Revenue - Total cost of revenue)
        gross_profit = statement_of_operations.copy()
        
        # Drop the row index ranges
        gross_profit.drop(gross_profit.index[15:], inplace=True)
        gross_profit.drop(gross_profit.index[7:13], inplace=True)
        gross_profit.drop(gross_profit.index[:6], inplace=True)
        
        # Reset Index
        gross_profit.reset_index(drop=True, inplace=True)

        #show results of Gross profit
        #st.write("Gross Profit from statement of Operation:")
        #st.write(gross_profit)

#Create Operating expenses 
        operating_expenses = statement_of_operations.copy()

        # Drop the row index ranges
        operating_expenses.drop(operating_expenses.index[20:], inplace=True)
        operating_expenses.drop(operating_expenses.index[:16], inplace=True)

        # Reset Index
        operating_expenses.reset_index(drop=True, inplace=True)

        #show results of Gross profit
#st.write("Operating Expenses:")
#st.write(operating_expenses)

#Creat Income before income taxes 
        income_before_income_taxes = statement_of_operations.copy()

 # Drop he row index ranges
        income_before_income_taxes.drop(income_before_income_taxes.index[25:], inplace=True)
        income_before_income_taxes.drop(income_before_income_taxes.index[:20], inplace=True)
        #show results of Gross profit
        #st.write("Income Before Income Taxes:")
#st.writ(income_before_income_taxes)

#Create Net Income 
        net_income = statement_of_operations.copy()

 # Drop the row index ranges
        net_income.drop(net_income.index[27:], inplace=True)
        net_income.drop(net_income.index[:24], inplace=True)

        #show results of Gross profit
        #st.write("Net Income:")
        #st.write(net_income)

# Start Working on the Statement of Comprehensive Income
        #Rename the column names
        statements_of_comprehensive_income.rename(columns={"Unnamed: 0": "December 31, 2023"}, inplace=True)
        statements_of_comprehensive_income.rename(columns={"Unnamed: 2": "December 31, 2022"}, inplace=True)
        statements_of_comprehensive_income.rename(columns={"Unnamed: 4": "December 31, 2021"}, inplace=True)
        
        #edit the values 
        value_at_0_to_2 = statements_of_comprehensive_income.iloc[0, 2]
        statements_of_comprehensive_income.iloc[0, 1] = value_at_0_to_2

        value_at_0_to_5 = statements_of_comprehensive_income.iloc[0, 5]
        statements_of_comprehensive_income.iloc[0, 3] = value_at_0_to_5

        value_at_0_to_8 = statements_of_comprehensive_income.iloc[0, 8]
        statements_of_comprehensive_income.iloc[0, 5] = value_at_0_to_8

        value_at_7_to_2 = statements_of_comprehensive_income.iloc[7, 2]
        statements_of_comprehensive_income.iloc[7, 1] = value_at_7_to_2

        value_at_7_to_5 = statements_of_comprehensive_income.iloc[7, 5]
        statements_of_comprehensive_income.iloc[7, 3] = value_at_7_to_5

        value_at_7_to_8 = statements_of_comprehensive_income.iloc[7, 8]
        statements_of_comprehensive_income.iloc[7, 5] = value_at_7_to_8

        #Delete columns
        statements_of_comprehensive_income.drop("Unnamed: 1", axis = 1 , inplace = True)
        statements_of_comprehensive_income.drop("Unnamed: 3", axis = 1 , inplace = True)
        statements_of_comprehensive_income.drop("Unnamed: 5", axis = 1 , inplace = True)
        statements_of_comprehensive_income.drop("Unnamed: 6", axis = 1 , inplace = True)
        statements_of_comprehensive_income.drop("Unnamed: 7", axis = 1 , inplace = True)

        #Remove Commas from the data set
        statements_of_comprehensive_income['December 31, 2023'] = statements_of_comprehensive_income['December 31, 2023'].str.replace(',', '', regex=False)
        statements_of_comprehensive_income['December 31, 2022'] = statements_of_comprehensive_income['December 31, 2022'].str.replace(',', '', regex=False)
        statements_of_comprehensive_income['December 31, 2021'] = statements_of_comprehensive_income['December 31, 2021'].str.replace(',', '', regex=False)

        #Drop the row
        statements_of_comprehensive_income.drop(statements_of_comprehensive_income.index[6:], inplace=True)
        statements_of_comprehensive_income.drop(statements_of_comprehensive_income.index[1], inplace=True)

        # Reset Index
        statements_of_comprehensive_income.reset_index(drop=True, inplace=True)


        #Show the results
        #st.write("Statements of Comprehensive Income:")
        #st.write(statements_of_comprehensive_income)

# Start Working on the Statement of Cash Flow
        #Rename the column names
        statement_of_cash_flow.rename(columns={"Unnamed: 0": "December 31, 2023"}, inplace=True)
        statement_of_cash_flow.rename(columns={"Unnamed: 2": "December 31, 2022"}, inplace=True)
        statement_of_cash_flow.rename(columns={"Unnamed: 4": "December 31, 2021"}, inplace=True)
        
        #edit the values 
        value_at_0_of_2 = statement_of_cash_flow.iloc[0, 2]
        statement_of_cash_flow.iloc[0, 1] = value_at_0_of_2

        value_at_0_of_5 = statement_of_cash_flow.iloc[0, 5]
        statement_of_cash_flow.iloc[0, 3] = value_at_0_of_5

        value_at_0_of_8 = statement_of_cash_flow.iloc[0, 8]
        statement_of_cash_flow.iloc[0, 5] = value_at_0_of_8

        value_at_43_to_2 = statement_of_cash_flow.iloc[43, 2]
        statement_of_cash_flow.iloc[43, 1] = value_at_43_to_2

        value_at_43_to_5 = statement_of_cash_flow.iloc[43, 5]
        statement_of_cash_flow.iloc[43, 3] = value_at_43_to_5

        value_at_43_to_8 = statement_of_cash_flow.iloc[43, 8]
        statement_of_cash_flow.iloc[43, 5] = value_at_43_to_8

        value_at_45_to_2 = statement_of_cash_flow.iloc[45, 2]
        statement_of_cash_flow.iloc[45, 1] = value_at_45_to_2

        value_at_45_to_5 = statement_of_cash_flow.iloc[45, 5]
        statement_of_cash_flow.iloc[45, 3] = value_at_45_to_5

        value_at_45_to_8 = statement_of_cash_flow.iloc[45, 8]
        statement_of_cash_flow.iloc[45, 5] = value_at_45_to_8

        value_at_47_to_2 = statement_of_cash_flow.iloc[47, 2]
        statement_of_cash_flow.iloc[47, 1] = value_at_47_to_2

        value_at_47_to_5 = statement_of_cash_flow.iloc[47, 5]
        statement_of_cash_flow.iloc[47, 3] = value_at_47_to_5

        value_at_47_to_8 = statement_of_cash_flow.iloc[47, 8]
        statement_of_cash_flow.iloc[47, 5] = value_at_47_to_8

        value_at_48_to_2 = statement_of_cash_flow.iloc[48, 2]
        statement_of_cash_flow.iloc[48, 1] = value_at_48_to_2

        value_at_48_to_5 = statement_of_cash_flow.iloc[48, 5]
        statement_of_cash_flow.iloc[48, 3] = value_at_48_to_5

        value_at_48_to_8 = statement_of_cash_flow.iloc[48, 8]
        statement_of_cash_flow.iloc[48, 5] = value_at_48_to_8


 #Delete columns
        statement_of_cash_flow.drop("Unnamed: 1", axis = 1 , inplace = True)
        statement_of_cash_flow.drop("Unnamed: 3", axis = 1 , inplace = True)
        statement_of_cash_flow.drop("Unnamed: 5", axis = 1 , inplace = True)
        statement_of_cash_flow.drop("Unnamed: 6", axis = 1 , inplace = True)
        statement_of_cash_flow.drop("Unnamed: 7", axis = 1 , inplace = True)

        #Remove Commas from the data set
        statement_of_cash_flow['December 31, 2023'] = statement_of_cash_flow['December 31, 2023'].str.replace(',', '', regex=False)
        statement_of_cash_flow['December 31, 2022'] = statement_of_cash_flow['December 31, 2022'].str.replace(',', '', regex=False)
        statement_of_cash_flow['December 31, 2021'] = statement_of_cash_flow['December 31, 2021'].str.replace(',', '', regex=False)

        #Drop the row
        statement_of_cash_flow.drop(statement_of_cash_flow.index[46], inplace=True)
        statement_of_cash_flow.drop(statement_of_cash_flow.index[44], inplace=True)
        statement_of_cash_flow.drop(statement_of_cash_flow.index[29], inplace=True)
        statement_of_cash_flow.drop(statement_of_cash_flow.index[17], inplace=True)
        statement_of_cash_flow.drop(statement_of_cash_flow.index[9], inplace=True)
        statement_of_cash_flow.drop(statement_of_cash_flow.index[1], inplace=True)

        # Reset Index
        statement_of_cash_flow.reset_index(drop=True, inplace=True)

        #Show the results
        #st.write("Statement of Cash Flow:") 
        #st.write(statement_of_cash_flow)

# Start Working on the Statement of Cash Flow from operating Activities
        cash_flow_of_operating_activities = statement_of_cash_flow.copy()

        #Drop the row
        cash_flow_of_operating_activities.drop(cash_flow_of_operating_activities.index[15:], inplace=True)

        #Show the results
        #st.write("Cash Flow From Operating Activities:")
        #st.write(cash_flow_of_operating_activities)

# Start Working on the Statement of Cash Flow from investing Activities
        cash_flow_of_investing_activities = statement_of_cash_flow.copy()

        #Drop the row
        cash_flow_of_investing_activities.drop(cash_flow_of_investing_activities.index[26:], inplace=True)
        cash_flow_of_investing_activities.drop(cash_flow_of_investing_activities.index[:15], inplace=True)

        # Reset Index
        cash_flow_of_investing_activities.reset_index(drop=True, inplace=True)

        #Show the results
        #st.write("Cash Flow From Investing Activities:")
        #st.write(cash_flow_of_investing_activities)

#start Working on the statement of Cash Flows from Financing Activities
        cash_flow_of_financing_activities = statement_of_cash_flow.copy()

        #Drop the row
        cash_flow_of_financing_activities.drop(cash_flow_of_financing_activities.index[40:], inplace=True)
        cash_flow_of_financing_activities.drop(cash_flow_of_financing_activities.index[:26], inplace=True)

        # Reset Index
        cash_flow_of_financing_activities.reset_index(drop=True, inplace=True)

        #Show the results
        #st.write("Cash Flow From Financing Activities:")
        #st.write(cash_flow_of_financing_activities)




        user_list = ["Over all" , "Balance Sheet" , "Statement of Operations"  , "Statement of Cash Flow"]
        selected_user = st.sidebar.selectbox("Show Analysis w.r.t" , user_list)

        if st.sidebar.button("Show Analysis"):
                helper.fetch_stats(uploaded_file, selected_user, total_assets, liabilities, total_revenue, total_cost_of_revenue, gross_profit, operating_expenses, income_before_income_taxes, net_income, statements_of_comprehensive_income, statement_of_cash_flow, cash_flow_of_operating_activities, cash_flow_of_investing_activities, cash_flow_of_financing_activities)
