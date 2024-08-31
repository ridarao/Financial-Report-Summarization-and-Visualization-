import streamlit as st
import plotly.express as px
import tabula
import pdfplumber
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation as punct
from heapq import nlargest

def process_pdf(uploaded_file, page_start=0, page_end=None):
    balance_sheet = None
    statement_of_operations = None
    statements_of_comprehensive_income = None
    statement_of_cash_flow = None
    if uploaded_file is not None:
        tables = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True)
        if len(tables) >= 5:
        # Select the 5th table (indexing starts from 0)
            balance_sheet = tables[5]
            statement_of_operations = tables[6]
            statements_of_comprehensive_income = tables[7]
            statement_of_cash_flow = tables[10]
        
        else:
            st.write("There are less than 5 tables in the PDF file.")

    return balance_sheet, statement_of_operations, statements_of_comprehensive_income, statement_of_cash_flow


def extract_and_summarize_from_pdf(uploaded_file, start_page=None, end_page=None, start_paragraph=None, end_paragraph=None):
    """
    Extract text from specified pages and paragraphs of a PDF file and summarize it.
    
    Args:
    - uploaded_file (file): PDF file uploaded.
    - start_page (int): Start page number (optional).
    - end_page (int): End page number (optional).
    - start_paragraph (int): Start paragraph number (optional).
    - end_paragraph (int): End paragraph number (optional).
    
    Returns:
    - str: Summarized text extracted from the specified pages and paragraphs.
    """
    
    if uploaded_file is None:
        return "No file uploaded."

    extracted_text = ""
    tables = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            if (start_page is None or page_num + 1 >= start_page) and (end_page is None or page_num + 1 <= end_page):
                page_text = page.extract_text()
                paragraphs = page_text.split('\n\n')
                if start_paragraph is None:
                    start_index = 0
                else:
                    start_index = max(0, start_paragraph - 1)
                if end_paragraph is None:
                    end_index = len(paragraphs)
                else:
                    end_index = min(len(paragraphs), end_paragraph)
                extracted_text += '\n\n'.join(paragraphs[start_index:end_index])

                # Extract tables from the page
                tables_on_page = tabula.read_pdf(uploaded_file, pages=page_num + 1, multiple_tables=True)
                if tables_on_page:
                    tables += tables_on_page

    if not extracted_text:
        return "No text extracted from the specified pages and paragraphs."

    # Exclude table text from the extracted text
    for table in tables:
        for row in table.iterrows():
            for cell_value in row[1].values:
                if cell_value and isinstance(cell_value, str) and cell_value.strip():
                    extracted_text = extracted_text.replace(cell_value, "").replace("  ", " ")

    # Text summarization
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(extracted_text)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punct:
            if word.text not in word_frequencies:
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if str(sent) not in sentence_scores:
                    sentence_scores[str(sent)] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[str(sent)] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.2)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    final_summary = ' '.join(summary)

    return final_summary



def fetch_stats(uploaded_file,selected_user,total_assets,liabilities,total_revenue,total_cost_of_revenue,gross_profit,operating_expenses,income_before_income_taxes,net_income,statements_of_comprehensive_income,statement_of_cash_flow,cash_flow_of_operating_activities,cash_flow_of_investing_activities,cash_flow_of_financing_activities):

    if selected_user == 'Over all':

#Balance Sheet table and graphs shown
        st.title("Financial Report Analysis and Summarization")
        st.header("Balance Sheet Analysis and Summarization")
        st.write("Total Asset Analysis and Summarization")
        
        #Spliting in two columns
        col1 , col2  = st.columns(2)
        with col1:
            st.write(total_assets)   
            

            
            #All total asset values add in it
            total_assets_values = total_assets.head(15)

            #Pie chart show in the form of visualization
            pie1 = px.pie(total_assets_values, names='Assets', values=total_assets_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Assets Pie plot ',
                labels={'Value': 'Value', 'Assets': 'Assets'})
        
            #Ploting of bar chart
            st.plotly_chart(pie1)
        
        with col2:
            #SUM of total assets show in the form of visualizations in bar chart
            total_assets_sum = total_assets.tail(1)
            #Reshape the data frame into a long format using the pd.melt function
            total_assets_sum_long = total_assets_sum.melt(id_vars='Assets', var_name='Date', value_name='Value')
        
            #bar plot figure 
            bar1 = px.bar(total_assets_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Assets bar plot Comperison between 2-Years',
                     labels={'Value':'Assets','Date':'Date'})
        
            #Ploting of bar chart
            st.plotly_chart(bar1)
        
            total_assets_values = total_assets.head(15)

        #Pie chart show in the form of visualization
            pie2 = px.pie(total_assets_values, names='Assets', values=total_assets_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Assets Pie plot ',
                labels={'Value': 'Value', 'Assets': 'Assets'})
        
        #Ploting of bar chart
            st.plotly_chart(pie2)
            
        final_summary = extract_and_summarize_from_pdf(uploaded_file,44,44,1,4)
            
        st.write("Summarization :", final_summary)
#Total Liabilities and Equity Graph and tables shown
        st.write("Total Laibilities & Equity Analysis and Summarization")

        #Spliting in two columns
        col3 , col4 = st.columns(2)
        with col3:
            st.write(liabilities)

            #All Laibility values add in this variable
            liabilities_values = liabilities.head(16)
        

        #Pie chart show in the form of visualization
            pie3 = px.pie(liabilities_values, names='Total Liabilities & Equity', values=liabilities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Liabilities & Equity Pie plot ',
                labels={'Value': 'Value', 'Total Liabilities & Equity': 'Total Liabilities & Equity'})
        
        #Ploting of bar chart
            st.plotly_chart(pie3)
        
        with col4:
            #SUM of liabilities show in the form of visualizations in bar chart
            liabilities_sum = liabilities.tail(1)
            liabilities_sum_long = liabilities_sum.melt(id_vars='Total Liabilities & Equity',var_name='Date', value_name='Value')

            #bar plot figure 
            bar2 = px.bar(liabilities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Laibilities and Equity bar plot Comperison between 2-Years',
                     labels={'Value':'Value','Date':'Date'})
        
            #Ploting of bar chart
            st.plotly_chart(bar2)

            #All Laibility values add in this variable
            liabilities_values = liabilities.head(16)
        

            #Pie chart show in the form of visualization
            pie4 = px.pie(liabilities_values, names='Total Liabilities & Equity', values=liabilities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Liabilities & Equity Pie plot ',
                labels={'Value': 'Value', 'Total Liabilities & Equity': 'Total Liabilities & Equity'})
        
            #Ploting of bar chart
            st.plotly_chart(pie4)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,90,90,0,1)
            
        st.write("Summarization :", final_summary)

#Statement of Operations Graph and tables shown
        st.header("Statement of Operations Analysis and Summarization")
        st.write("Total Revenue Analysis and Summarization")

        #Spliting in two columns
        col5 , col6 = st.columns(2)
        with col5:
            st.write(total_revenue)

            #All Revenue values add in this variable
            revenue_values = total_revenue.head(5)
        
        #Pie chart show in the form of visualization
            pie5 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
              title='Total Revenues Pie plot ',
              labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
            st.plotly_chart(pie5)

        with col6:
            #SUM of Total Revenue show in the form of visualizations in bar chart
            total_revenue_sum = total_revenue.tail(1)
            total_revenue_sum_long = total_revenue_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar3 = px.bar(total_revenue_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Revenues bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar3)

            #All Revenue values add in this variable
            revenue_values = total_revenue.head(5)
        
            #Pie chart show in the form of visualization
            pie6 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Revenues Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie6)

        #Pie chart show in the form of visualization
        pie7 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Revenues Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie7)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,34,34,0,1)
            
        st.write("Summarization :", final_summary)        


#Total cost of Revenue graph and table shown
        st.write("Total cost of Revenue Analysis and Summarization")

        #Spliting in two columns
        col7 , col8 = st.columns(2)
        with col7:
            st.write(total_cost_of_revenue)

            #All Revenue values add in this variable
            cost_of_revenue_values = total_cost_of_revenue.head(4)
        
            #Pie chart show in the form of visualization
            pie8 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie8)
            

        with col8:
            
            total_cost_of_revenue_sum = total_cost_of_revenue.tail(1)
            total_cost_of_revenue_sum_long = total_cost_of_revenue_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar4 = px.bar(total_cost_of_revenue_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cost of Revenues bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar4)

            #All Revenue values add in this variable
            cost_of_revenue_values = total_cost_of_revenue.head(4)
        
            #Pie chart show in the form of visualization
            pie9 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie9)
        
        #Pie chart show in the form of visualization
        pie10 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie10)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,41,41,0,1)
            
        st.write("Summarization :", final_summary)

#Total Gross profit graph and table shown
        st.write("Gross Profit Analysis and Summarization")

        #Spliting in two columns
        col9 , col10 = st.columns(2)
        with col9:
            st.write(gross_profit)

            #All Revenue values add in this variable
            gross_profit_values = gross_profit.head(2)
        
            #Pie chart show in the form of visualization
            pie11 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Gross Profit'})
        
            #Ploting of bar chart
            st.plotly_chart(pie11)

        with col10:

            gross_profit_sum = gross_profit.tail(1)
            gross_profit_sum_long = gross_profit_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar5 = px.bar(gross_profit_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Gross Profit bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar5)

            #All Revenue values add in this variable
            gross_profit_values = gross_profit.head(2)
        
            #Pie chart show in the form of visualization
            pie12 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie12)
        
        #Pie chart show in the form of visualization
        pie13 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie13)

        
#Total Operating expenses of graph and table shown
        st.write("Operating Expenses of Analysis and Summarization")

        #Spliting in two columns
        col11 , col12 = st.columns(2)
        with col11:
            st.write(operating_expenses)

            #All Revenue values add in this variable
            operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
            pie14 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
            st.plotly_chart(pie14)

        with col12:
            operating_expenses_sum = operating_expenses.tail(1)
            operating_expenses_sum_long = operating_expenses_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar6 = px.bar(operating_expenses_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Operating Expenses bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar6)

            #All Revenue values add in this variable
            operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
            pie15 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
            st.plotly_chart(pie15)

        #All Revenue values add in this variable
        operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
        pie16 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
        st.plotly_chart(pie16)   

#Total Income Before Income Taxes of graph and table shown
        st.write("Income Before Income Taxes of Analysis and Summarization")

        #Spliting in two columns
        col13 , col14 = st.columns(2)
        
        with col13:
            st.write(income_before_income_taxes)
            
            #All Revenue values add in this variable
            income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
            pie17 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Taxes 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Income before tax'})
        
            #Ploting of bar chart
            st.plotly_chart(pie17)

        with col14:
            income_before_income_taxes_sum = income_before_income_taxes.tail(1)
            income_before_income_taxes_sum_long = income_before_income_taxes_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar7 = px.bar(income_before_income_taxes_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Income Before Taxes bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar7)

            #All Revenue values add in this variable
            income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
            pie18 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Expenses 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
            st.plotly_chart(pie18)

        #All Revenue values add in this variable
        income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
        pie19 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Taxes 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
        st.plotly_chart(pie19)
        
#Total Net Income of graph and table shown

        st.write("Net Income of Analysis and Summarization")

        #Spliting in two columns
        col15 , col16 = st.columns(2)
        
        with col15:
            st.write(net_income)
            
            #All Revenue values add in this variable
            net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
            pie20 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Net Income'})
        
            #Ploting of bar chart
            st.plotly_chart(pie20)

        with col16:
            net_income_sum = net_income.tail(1)
            net_income_sum_long = net_income_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar8 = px.bar(net_income_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Net Income bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar8)

            #All Revenue values add in this variable
            net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
            pie21 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
            st.plotly_chart(pie21)

        #All Revenue values add in this variable
        net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
        pie22 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income Income'})
        
            #Ploting of bar chart
        st.plotly_chart(pie22)

#Total Statements of Comprehensive Income of graph and table shown
        # st.header("Statements of Comprehensive Income Analysis and Summarization")
        
        # #Spliting in two columns
        # col17 , col18 = st.columns(2)
        
        # with col17:
        #     st.write(statements_of_comprehensive_income)
            
        #     #All Revenue values add in this variable
        #     statements_of_comprehensive_income = statements_of_comprehensive_income.rename(columns = {"'Tesla, Inc.\rConsolidated Statements of Comprehensive Income\r(in millions)\rYear Ended December 31,\r202320222021\rNet income$14,974$12,587$5,644\rOther comprehensive income (loss):\rForeign currency translation adjustment198(392)(308)\rUnrealized net gain (loss) on investments16(23)(1)\rAdjustment for net loss realized and included in net income4——\rComprehensive income15,19212,1725,335\rLess: Comprehensive (loss) income attributable to noncontrolling interests and\rredeemable noncontrolling interests in subsidiaries(23)31125\rComprehensive income attributable to common stockholders\r$15,215$12,141$5,210\rThe accompanying notes are an integral part of these consolidated financial statements.\r51', 'December 31, 2023', 'December 31, 2022', 'December 31, 2021'":"Statement of Comprehensive Income"})
        #     statements_of_comprehensive_income_values = statements_of_comprehensive_income.head(4)
        
        #     #Pie chart show in the form of visualization
            
        #     pie23 = px.pie(statements_of_comprehensive_income_values, names="Statement of Comprehensive Income", values=statements_of_comprehensive_income_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
        #         title='Statements of Comprehensive Income 2023 Pie plot ',
        #         labels={'Value': 'Value', 'Revenues': 'Statements of Comprehensive Income'})
        
        #     #Ploting of bar chart
        #     st.plotly_chart(pie23)


        # with col18:
        #     statements_of_comprehensive_income_sum = statements_of_comprehensive_income.tail(1)
        #     statements_of_comprehensive_income_sum_long = statements_of_comprehensive_income_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

        #     #Bar plot figure
        #     bar9 = px.bar(statements_of_comprehensive_income_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
        #              title='Statements of Comprehensive Income bar plot Comperison between 3-Years',
        #              labels={'Value':'Value','Date':'Date'})
            
        #     #Ploting of bar chart
        #     st.plotly_chart(bar9)

        #     #All Revenue values add in this variable
        #     statements_of_comprehensive_income_values = statements_of_comprehensive_income.head(4)
        
        #     #Pie chart show in the form of visualization
        #     pie24 = px.pie(statements_of_comprehensive_income_values, names="'Tesla, Inc.\rConsolidated Statements of Comprehensive Income\r(in millions)\rYear Ended December 31,\r202320222021\rNet income$14,974$12,587$5,644\rOther comprehensive income (loss):\rForeign currency translation adjustment198(392)(308)\rUnrealized net gain (loss) on investments16(23)(1)\rAdjustment for net loss realized and included in net income4——\rComprehensive income15,19212,1725,335\rLess: Comprehensive (loss) income attributable to noncontrolling interests and\rredeemable noncontrolling interests in subsidiaries(23)31125\rComprehensive income attributable to common stockholders\r$15,215$12,141$5,210\rThe accompanying notes are an integral part of these consolidated financial statements.\r51', 'December 31, 2023', 'December 31, 2022', 'December 31, 2021'", values=statements_of_comprehensive_income_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
        #         title='Statements of Comprehensive Income 2022 Pie plot ',
        #         labels={'Value': 'Value', 'Revenues': 'Statements of Comprehensive Income'})
        
        #     #Ploting of bar chart
        #     st.plotly_chart(pie24)

        # #All Revenue values add in this variable
        # statements_of_comprehensive_income_values = statements_of_comprehensive_income.head(4)
        
        #     #Pie chart show in the form of visualization
        # pie25 = px.pie(statements_of_comprehensive_income_values, names="'Tesla, Inc.\rConsolidated Statements of Comprehensive Income\r(in millions)\rYear Ended December 31,\r202320222021\rNet income$14,974$12,587$5,644\rOther comprehensive income (loss):\rForeign currency translation adjustment198(392)(308)\rUnrealized net gain (loss) on investments16(23)(1)\rAdjustment for net loss realized and included in net income4——\rComprehensive income15,19212,1725,335\rLess: Comprehensive (loss) income attributable to noncontrolling interests and\rredeemable noncontrolling interests in subsidiaries(23)31125\rComprehensive income attributable to common stockholders\r$15,215$12,141$5,210\rThe accompanying notes are an integral part of these consolidated financial statements.\r51', 'December 31, 2023', 'December 31, 2022', 'December 31, 2021'", values=statements_of_comprehensive_income_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
        #         title='Statements of Comprehensive Income 2021 Pie plot ',
        #         labels={'Value': 'Value', 'Revenues': 'Total Income Income'})
        
        #     #Ploting of bar chart
        # st.plotly_chart(pie25)



#Total Statements of Cash Flow of operating activities of graph and table shown
        st.header("Statement of Cash Flow of Analysis and Summarization")
        st.write("Cash Flow of Operating Activities of Analysis and Summarization")
        

        #Spliting in two columns
        col19 , col20 = st.columns(2)
        
        with col19:
            st.write(cash_flow_of_operating_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
             #Pie chart show in the form of visualization
            pie26 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by operating activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie26)

        with col20:
            cash_flow_of_operating_activities_sum = cash_flow_of_operating_activities.tail(1)
            cash_flow_of_operating_activities_sum_long = cash_flow_of_operating_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar10 = px.bar(cash_flow_of_operating_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Operating activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar10)

            #All Revenue values add in this variable
            cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
            #Pie chart show in the form of visualization
            pie27 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by operating activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie27)

        #All Revenue values add in this variable
        cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
            #Pie chart show in the form of visualization
        pie28 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by operating activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie28)

#Total Statements of Cash Flow of investing activities of graph and table shown
        st.write("Cash Flow of Investing Activities of Analysis and Summarization")
        

        #Spliting in two columns
        col21 , col22 = st.columns(2)
        
        with col21:
            st.write(cash_flow_of_investing_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
             #Pie chart show in the form of visualization
            pie29 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by Investing activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by investing activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie29)

        with col22:
            cash_flow_of_investing_activities_sum = cash_flow_of_investing_activities.tail(1)
            cash_flow_of_investing_activities_sum_long = cash_flow_of_investing_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar11 = px.bar(cash_flow_of_investing_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Investing activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar11)

            #All Revenue values add in this variable
            cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
            #Pie chart show in the form of visualization
            pie30 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Investing activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Investing activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie30)

        #All Revenue values add in this variable
        cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
            #Pie chart show in the form of visualization
        pie31 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Investing activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Investing activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie31)

#Total Statements of Cash Flow of Financing activities of graph and table shown
        st.write("Cash Flow of Financing Activities of Analysis and Summarization")
        
        #Spliting in two columns
        col23 , col24 = st.columns(2)
        
        with col23:
            st.write(cash_flow_of_financing_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(13)
        
             #Pie chart show in the form of visualization
            pie32 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by Financing activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie32)

        with col24:
            cash_flow_of_financing_activities_sum = cash_flow_of_financing_activities.tail(1)
            cash_flow_of_financing_activities_sum_long = cash_flow_of_financing_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar12 = px.bar(cash_flow_of_financing_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Financing activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar12)

            #All Revenue values add in this variable
            cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(13)
        
            #Pie chart show in the form of visualization
            pie33 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Financing activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie33)

        #All Revenue values add in this variable
        cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(10)
        
            #Pie chart show in the form of visualization
        pie34 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Financing activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie34)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,45,45,0,1)
            
        st.write("Summarization :", final_summary) 
                                                                
                                                                
                                                                
                                                                #Scroll Bar Option 2
#Balance Sheet of graph and table visualization
    elif selected_user == 'Balance Sheet':
        st.header("Total Asset Analysis and Summarization")

        #Spliting in two columns
        col1 , col2  = st.columns(2)
        with col1:
            st.write(total_assets)

            #All total asset values add in it
            total_assets_values = total_assets.head(15)

            #Pie chart show in the form of visualization
            pie1 = px.pie(total_assets_values, names='Assets', values=total_assets_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Assets Pie plot ',
                labels={'Value': 'Value', 'Assets': 'Assets'})
        
            #Ploting of bar chart
            st.plotly_chart(pie1)
        
        with col2:
            #SUM of total assets show in the form of visualizations in bar chart
            total_assets_sum = total_assets.tail(1)
            #Reshape the data frame into a long format using the pd.melt function
            total_assets_sum_long = total_assets_sum.melt(id_vars='Assets', var_name='Date', value_name='Value')
        
            #bar plot figure 
            bar1 = px.bar(total_assets_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Assets bar plot Comperison between 2-Years',
                     labels={'Value':'Assets','Date':'Date'})
        
            #Ploting of bar chart
            st.plotly_chart(bar1)
        
            total_assets_values = total_assets.head(15)

        #Pie chart show in the form of visualization
            pie2 = px.pie(total_assets_values, names='Assets', values=total_assets_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Assets Pie plot ',
                labels={'Value': 'Value', 'Assets': 'Assets'})
            
        #Ploting of bar chart
            st.plotly_chart(pie2)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,44,44,1,4)
            
        st.write("Summarization :", final_summary)

           

#Laibilities graph and table visualization
        st.header("Total Laibilities Analysis and Summarization")
        
        #Spliting in two columns
        col3 , col4 = st.columns(2)
        with col3:
            st.write(liabilities)

            #All Laibility values add in this variable
            liabilities_values = liabilities.head(16)
        

        #Pie chart show in the form of visualization
            pie3 = px.pie(liabilities_values, names='Total Liabilities & Equity', values=liabilities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Liabilities & Equity Pie plot ',
                labels={'Value': 'Value', 'Total Liabilities & Equity': 'Total Liabilities & Equity'})
        
        #Ploting of bar chart
            st.plotly_chart(pie3)
        
        with col4:
            #SUM of liabilities show in the form of visualizations in bar chart
            liabilities_sum = liabilities.tail(1)
            liabilities_sum_long = liabilities_sum.melt(id_vars='Total Liabilities & Equity',var_name='Date', value_name='Value')

            #bar plot figure 
            bar2 = px.bar(liabilities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Laibilities and Equity bar plot Comperison between 2-Years',
                     labels={'Value':'Value','Date':'Date'})
        
            #Ploting of bar chart
            st.plotly_chart(bar2)

            #All Laibility values add in this variable
            liabilities_values = liabilities.head(16)
        

            #Pie chart show in the form of visualization
            pie4 = px.pie(liabilities_values, names='Total Liabilities & Equity', values=liabilities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Liabilities & Equity Pie plot ',
                labels={'Value': 'Value', 'Total Liabilities & Equity': 'Total Liabilities & Equity'})
        
            #Ploting of bar chart
            st.plotly_chart(pie4)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,90,90,0,1)
            
        st.write("Summarization :", final_summary)                                                    
                                                            
                                                            
                                                            #Scroll bar of option 3
#Statement of Operation All tables and graph visualize.
    elif selected_user == 'Statement of Operations':
        st.header("Statement of Operation Analysis and Summarization")

#Total Revenue tables and graph visualization
        st.write("Total Revenue Analysis and Summarization")

         #Spliting in two columns
        col5 , col6 = st.columns(2)
        with col5:
            st.write(total_revenue)

            #All Revenue values add in this variable
            revenue_values = total_revenue.head(5)
        
        #Pie chart show in the form of visualization
            pie5 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
              title='Total Revenues Pie plot ',
              labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
            st.plotly_chart(pie5)

        with col6:
            #SUM of Total Revenue show in the form of visualizations in bar chart
            total_revenue_sum = total_revenue.tail(1)
            total_revenue_sum_long = total_revenue_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar3 = px.bar(total_revenue_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Revenues bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar3)

            #All Revenue values add in this variable
            revenue_values = total_revenue.head(5)
        
            #Pie chart show in the form of visualization
            pie6 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Revenues Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie6)

        #Pie chart show in the form of visualization
        pie7 = px.pie(revenue_values, names='Revenues', values=revenue_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Revenues Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie7)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,34,34,0,1)
            
        st.write("Summarization :", final_summary) 

#Total Cost of Revenue table and graph visualization
        st.header("Total cost of Revenue Analysis and Summarization")
        
        #Spliting in two columns
        col7 , col8 = st.columns(2)
        with col7:
            st.write(total_cost_of_revenue)

            #All Revenue values add in this variable
            cost_of_revenue_values = total_cost_of_revenue.head(4)
        
            #Pie chart show in the form of visualization
            pie8 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie8)
            

        with col8:
            
            total_cost_of_revenue_sum = total_cost_of_revenue.tail(1)
            total_cost_of_revenue_sum_long = total_cost_of_revenue_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar4 = px.bar(total_cost_of_revenue_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cost of Revenues bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar4)

            #All Revenue values add in this variable
            cost_of_revenue_values = total_cost_of_revenue.head(4)
        
            #Pie chart show in the form of visualization
            pie9 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie9)
        
        #Pie chart show in the form of visualization
        pie10 = px.pie(cost_of_revenue_values, names='Revenues', values=cost_of_revenue_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cost of Revenues 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie10)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,41,41,0,1)
            
        st.write("Summarization :", final_summary)

#Gross profit tables and graph visualization
        st.header("Gross Profit Analysis and Summarization")
        
        #Spliting in two columns
        col9 , col10 = st.columns(2)
        with col9:
            st.write(gross_profit)

            #All Revenue values add in this variable
            gross_profit_values = gross_profit.head(2)
        
            #Pie chart show in the form of visualization
            pie11 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Gross Profit'})
        
            #Ploting of bar chart
            st.plotly_chart(pie11)

        with col10:

            gross_profit_sum = gross_profit.tail(1)
            gross_profit_sum_long = gross_profit_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar5 = px.bar(gross_profit_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Gross Profit bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar5)

            #All Revenue values add in this variable
            gross_profit_values = gross_profit.head(2)
        
            #Pie chart show in the form of visualization
            pie12 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
            #Ploting of bar chart
            st.plotly_chart(pie12)
        
        #Pie chart show in the form of visualization
        pie13 = px.pie(gross_profit_values, names='Revenues', values=gross_profit_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Gross Profit 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Revenues'})
        
        #Ploting of bar chart
        st.plotly_chart(pie13)

#Operating tables and graph visualization
        st.header("Operating Expenses of Analysis and Summarization")
        
        #Spliting in two columns
        col11 , col12 = st.columns(2)
        with col11:
            st.write(operating_expenses)

            #All Revenue values add in this variable
            operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
            pie14 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
            st.plotly_chart(pie14)

        with col12:
            operating_expenses_sum = operating_expenses.tail(1)
            operating_expenses_sum_long = operating_expenses_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar6 = px.bar(operating_expenses_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Operating Expenses bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar6)

            #All Revenue values add in this variable
            operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
            pie15 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
            st.plotly_chart(pie15)

        #All Revenue values add in this variable
        operating_expenses_values = operating_expenses.head(2)
        
            #Pie chart show in the form of visualization
        pie16 = px.pie(operating_expenses_values, names='Revenues', values=operating_expenses_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Operating Expenses 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Operating expenses'})
        
            #Ploting of bar chart
        st.plotly_chart(pie16)

#Income before taxes tables and graph visualization
        st.header("Income Before Income Taxes of Analysis and Summarization")
        
        #Spliting in two columns
        col13 , col14 = st.columns(2)
        
        with col13:
            st.write(income_before_income_taxes)
            
            #All Revenue values add in this variable
            income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
            pie17 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Taxes 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Income before tax'})
        
            #Ploting of bar chart
            st.plotly_chart(pie17)

        with col14:
            income_before_income_taxes_sum = income_before_income_taxes.tail(1)
            income_before_income_taxes_sum_long = income_before_income_taxes_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar7 = px.bar(income_before_income_taxes_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Income Before Taxes bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar7)

            #All Revenue values add in this variable
            income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
            pie18 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Expenses 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
            st.plotly_chart(pie18)

        #All Revenue values add in this variable
        income_before_income_taxes_values = income_before_income_taxes.head(4)
        
            #Pie chart show in the form of visualization
        pie19 = px.pie(income_before_income_taxes_values, names='Revenues', values=income_before_income_taxes_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Income Before Taxes 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
        st.plotly_chart(pie19)

#Net Income tables and graph visualization
        st.header("Net Income of Analysis and Summarization")
        
        #Spliting in two columns
        col15 , col16 = st.columns(2)
        
        with col15:
            st.write(net_income)
            
            #All Revenue values add in this variable
            net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
            pie20 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2023 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Net Income'})
        
            #Ploting of bar chart
            st.plotly_chart(pie20)

        with col16:
            net_income_sum = net_income.tail(1)
            net_income_sum_long = net_income_sum.melt(id_vars='Revenues' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar8 = px.bar(net_income_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Net Income bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar8)

            #All Revenue values add in this variable
            net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
            pie21 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income before Taxes'})
        
            #Ploting of bar chart
            st.plotly_chart(pie21)

        #All Revenue values add in this variable
        net_income_values = net_income.head(2)
        
            #Pie chart show in the form of visualization
        pie22 = px.pie(net_income_values, names='Revenues', values=net_income_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Net Income 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Total Income Income'})
        
            #Ploting of bar chart
        st.plotly_chart(pie22)

    # elif selected_user == 'Statement of Comprehensive Income':
    #     st.header("Statements of Comprehensive Income Analysis and Summarization")
    #     st.write(statements_of_comprehensive_income)


                                                            
                                                            
                                                            
                                                            #Scroll Bar of Option 3
#Statement of Cash flow All the tables analysis and summarization
    elif selected_user == 'Statement of Cash Flow':
        st.title("Statement of Cash Flow of Analysis and Summarization")

#Cash Flow of Operating Activities tables and graph visualization
        st.header("Cash Flow of Operating Activities of Analysis and Summarization")
        
        #Spliting in two columns
        col19 , col20 = st.columns(2)
        
        with col19:
            st.write(cash_flow_of_operating_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
             #Pie chart show in the form of visualization
            pie26 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by operating activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie26)

        with col20:
            cash_flow_of_operating_activities_sum = cash_flow_of_operating_activities.tail(1)
            cash_flow_of_operating_activities_sum_long = cash_flow_of_operating_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar10 = px.bar(cash_flow_of_operating_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Operating activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar10)

            #All Revenue values add in this variable
            cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
            #Pie chart show in the form of visualization
            pie27 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by operating activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie27)

        #All Revenue values add in this variable
        cash_flow_of_operating_activities_values = cash_flow_of_operating_activities.head(14)
        
            #Pie chart show in the form of visualization
        pie28 = px.pie(cash_flow_of_operating_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_operating_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by operating activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by operating activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie28)

#Cash flow of investing activities tables and graph visualization
        st.header("Cash Flow of Investing Activities of Analysis and Summarization")
        
        #Spliting in two columns
        col21 , col22 = st.columns(2)
        
        with col21:
            st.write(cash_flow_of_investing_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
             #Pie chart show in the form of visualization
            pie29 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by Investing activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by investing activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie29)

        with col22:
            cash_flow_of_investing_activities_sum = cash_flow_of_investing_activities.tail(1)
            cash_flow_of_investing_activities_sum_long = cash_flow_of_investing_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar11 = px.bar(cash_flow_of_investing_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Investing activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar11)

            #All Revenue values add in this variable
            cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
            #Pie chart show in the form of visualization
            pie30 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Investing activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Investing activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie30)

        #All Revenue values add in this variable
        cash_flow_of_investing_activities_values = cash_flow_of_investing_activities.head(10)
        
            #Pie chart show in the form of visualization
        pie31 = px.pie(cash_flow_of_investing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_investing_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Investing activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Investing activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie31)

#cash flow of financing actiovities tables and graph visualization
        st.header("Cash Flow of Financing Activities of Analysis and Summarization")
        
        #Spliting in two columns
        col23 , col24 = st.columns(2)
        
        with col23:
            st.write(cash_flow_of_financing_activities)
            
             #All Revenue values add in this variable
            cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(13)
        
             #Pie chart show in the form of visualization
            pie32 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2023'], color_discrete_sequence = px.colors.qualitative.Pastel,
                 title='Total Cash Flow by Financing activities 2023 Pie plot ',
                 labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
             #Ploting of bar chart
            st.plotly_chart(pie32)

        with col24:
            cash_flow_of_financing_activities_sum = cash_flow_of_financing_activities.tail(1)
            cash_flow_of_financing_activities_sum_long = cash_flow_of_financing_activities_sum.melt(id_vars='Cash Flows from Operating Activities' , var_name='Date', value_name='Value')

            #Bar plot figure
            bar12 = px.bar(cash_flow_of_financing_activities_sum_long, x='Date',y='Value', color_discrete_sequence = px.colors.qualitative.Pastel,
                     title='Total Cash Flow by Financing activities bar plot Comperison between 3-Years',
                     labels={'Value':'Value','Date':'Date'})
            
            #Ploting of bar chart
            st.plotly_chart(bar12)

            #All Revenue values add in this variable
            cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(13)
        
            #Pie chart show in the form of visualization
            pie33 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2022'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Financing activities 2022 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
            #Ploting of bar chart
            st.plotly_chart(pie33)

        #All Revenue values add in this variable
        cash_flow_of_financing_activities_values = cash_flow_of_financing_activities.head(10)
        
            #Pie chart show in the form of visualization
        pie34 = px.pie(cash_flow_of_financing_activities_values, names='Cash Flows from Operating Activities', values=cash_flow_of_financing_activities_values['December 31, 2021'], color_discrete_sequence = px.colors.qualitative.Pastel,
                title='Total Cash Flow by Financing activities 2021 Pie plot ',
                labels={'Value': 'Value', 'Revenues': 'Cash Flow by Financing activities'})
        
            #Ploting of bar chart
        st.plotly_chart(pie34)

        final_summary = extract_and_summarize_from_pdf(uploaded_file,45,45,0,1)
            
        st.write("Summarization :", final_summary)


    else:
        st.write("Nothing is show")
