Latest June 14


# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# import os
# import pandas as pd
# from linkedin_api import Linkedin
# from urllib.parse import urlparse
# import json
# import logging

# app = Flask(__name__)

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'xlsx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def extract_company_name(linkedin_url):
#     parsed_url = urlparse(linkedin_url)
#     path_segments = [
#         segment for segment in parsed_url.path.split('/') if segment]

#     if 'company' in path_segments:
#         company_index = path_segments.index('company')
#         if company_index < len(path_segments) - 1:
#             return path_segments[company_index + 1]

#     return None


# def fetch_company_details(api, company_name, linkedin_url):
#     try:
#         company_data = api.get_company(company_name)
#         return json.loads(json.dumps(company_data, indent=2))
#     except Exception as e:
#         logger.error(
#             f"Error fetching details for {company_name} from {linkedin_url}: {str(e)}")
#         return None


# def convert_to_billion_million(value):
#     if value is None:
#         return None

#     try:
#         value = float(value)
#     except (ValueError, TypeError):
#         return f"{value}"

#     billion_threshold = 1_000_000_000
#     million_threshold = 1_000_000

#     if value >= billion_threshold:
#         return f"{value / billion_threshold:.2f}B"
#     elif value >= million_threshold:
#         return f"{value / million_threshold:.2f}M"
#     else:
#         return f"{value:.2f}"


# def process_urls(api, linkedin_urls_df):
#     all_company_details = []

#     for _, row in linkedin_urls_df.iterrows():
#         linkedin_url = row['LinkedIn URL']
#         company_name = extract_company_name(linkedin_url)

#         if company_name:
#             company_data = fetch_company_details(
#                 api, company_name, linkedin_url)

#             if company_data:
#                 try:
#                     employee_range_start = company_data.get(
#                         'staffCountRange', {}).get('start')
#                     employee_range_end = company_data.get(
#                         'staffCountRange', {}).get('end')
#                     funds = company_data.get('fundingData', {}).get(
#                         'lastFundingRound', {}).get('moneyRaised', {}).get('amount', " ")
#                     converted_funds = convert_to_billion_million(funds)
#                     industry = company_data.get('companyIndustries', [{}])[
#                         0].get('localizedName')
#                     hq = company_data.get('headquarter', {}).get('country')
#                     specialities = company_data.get('specialities')
#                     mem = company_data.get('staffCount')
#                     des = company_data.get('description')
#                     founded = company_data.get('foundedOn', {}).get('year')

#                     company_details = {
#                         'Company name': company_name,
#                         'Company Domain': company_data.get("companyPageUrl"),
#                         'Founded': founded,
#                         'ECR_start': employee_range_start,
#                         'ECR_End': employee_range_end,
#                         'Associated_members': mem,
#                         'Industry': industry,
#                         'HQ': hq,
#                         'Funds': converted_funds,
#                         'Description': des,
#                         'Specialities': specialities
#                     }

#                     all_company_details.append(company_details)
#                 except Exception as e:
#                     logger.error(
#                         f"Error extracting details for {company_name} from {linkedin_url}: {str(e)}")
#             else:
#                 logger.warning(
#                     f"No data fetched for {company_name} from {linkedin_url}.")

#     return pd.DataFrame(all_company_details)


# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)

#         file = request.files['file']

#         if file.filename == '':
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             filename = os.path.join(app.config['UPLOAD_FOLDER'], 'urls.xlsx')
#             file.save(filename)

#             linkedin_email = request.form['email']
#             linkedin_password = request.form['password']

#             if not linkedin_password:
#                 return render_template('index.html', error='Password cannot be empty.')

#             try:
#                 api = Linkedin(linkedin_email, linkedin_password)

#                 linkedin_urls_df = pd.read_excel(filename)
#                 processed_data = process_urls(api, linkedin_urls_df)

#                 output_filename = 'companies_data_with_details.xlsx'
#                 output_filepath = os.path.join(
#                     app.config['UPLOAD_FOLDER'], output_filename)

#                 processed_data.to_excel(output_filepath, index=False)

#                 return render_template('index.html', success=True, output_filename=output_filename)
#             except Exception as e:
#                 error_message = f"Error: {str(e)}"

#                 logger.error(error_message)
#                 return render_template('index.html', error=error_message)

#     return render_template('index.html', success=False)


# if __name__ == '__main__':
#     app.run(debug=True)
# ----------------------------------------------------------------------------------

# from flask import Flask, render_template, request, redirect, url_for, send_file
# import os
# import pandas as pd
# from linkedin_api import Linkedin
# from urllib.parse import urlparse
# import json
# import logging

# app = Flask(__name__)

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# ALLOWED_EXTENSIONS = {'xlsx'}


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def extract_company_name(linkedin_url):
#     parsed_url = urlparse(linkedin_url)
#     path_segments = [
#         segment for segment in parsed_url.path.split('/') if segment]

#     if 'company' in path_segments:
#         company_index = path_segments.index('company')
#         if company_index < len(path_segments) - 1:
#             return path_segments[company_index + 1]

#     return None


# def fetch_company_details(api, company_name, linkedin_url):
#     try:
#         company_data = api.get_company(company_name)
#         return json.loads(json.dumps(company_data, indent=2))
#     except Exception as e:
#         logger.error(
#             f"Error fetching details for {company_name} from {linkedin_url}: {str(e)}")
#         return None


# def convert_to_billion_million(value):
#     if value is None:
#         return None

#     try:
#         value = float(value)
#     except (ValueError, TypeError):
#         return f"{value}"

#     billion_threshold = 1_000_000_000
#     million_threshold = 1_000_000

#     if value >= billion_threshold:
#         return f"{value / billion_threshold:.2f}B"
#     elif value >= million_threshold:
#         return f"{value / million_threshold:.2f}M"
#     else:
#         return f"{value:.2f}"


# def process_urls(api, linkedin_urls_df):
#     all_company_details = []

#     for _, row in linkedin_urls_df.iterrows():
#         linkedin_url = row['LinkedIn URL']
#         company_name = extract_company_name(linkedin_url)

#         if company_name:
#             company_data = fetch_company_details(
#                 api, company_name, linkedin_url)

#             if company_data:
#                 try:
#                     employee_range_start = company_data.get(
#                         'staffCountRange', {}).get('start')
#                     employee_range_end = company_data.get(
#                         'staffCountRange', {}).get('end')
#                     funds = company_data.get('fundingData', {}).get(
#                         'lastFundingRound', {}).get('moneyRaised', {}).get('amount', " ")
#                     converted_funds = convert_to_billion_million(funds)
#                     industry = company_data.get('companyIndustries', [{}])[
#                         0].get('localizedName')
#                     hq = company_data.get('headquarter', {}).get('country')
#                     specialities = company_data.get('specialities')
#                     mem = company_data.get('staffCount')
#                     des = company_data.get('description')
#                     founded = company_data.get('foundedOn', {}).get('year')

#                     company_details = {
#                         'Company name': company_name,
#                         'Company Domain': company_data.get("companyPageUrl"),
#                         'Founded': founded,
#                         'ECR_start': employee_range_start,
#                         'ECR_End': employee_range_end,
#                         'Associated_members': mem,
#                         'Industry': industry,
#                         'HQ': hq,
#                         'Funds': converted_funds,
#                         'Description': des,
#                         'Specialities': specialities
#                     }

#                     all_company_details.append(company_details)
#                 except Exception as e:
#                     logger.error(
#                         f"Error extracting details for {company_name} from {linkedin_url}: {str(e)}")
#             else:
#                 logger.warning(
#                     f"No data fetched for {company_name} from {linkedin_url}.")

#     return pd.DataFrame(all_company_details)


# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     return send_file(filename, as_attachment=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)

#         file = request.files['file']

#         if file.filename == '':
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             filename = 'urls.xlsx'
#             file.save(filename)

#             linkedin_email = request.form['email']
#             linkedin_password = request.form['password']

#             if not linkedin_password:
#                 return render_template('index.html', error='Password cannot be empty.')

#             try:
#                 api = Linkedin(linkedin_email, linkedin_password)

#                 linkedin_urls_df = pd.read_excel(filename)
#                 processed_data = process_urls(api, linkedin_urls_df)

#                 output_filename = 'companies_data_with_details.xlsx'
#                 processed_data.to_excel(output_filename, index=False)

#                 return render_template('index.html', success=True, output_filename=output_filename)
#             except Exception as e:
#                 error_message = f"Error: {str(e)}"

#                 logger.error(error_message)
#                 return render_template('index.html', error=error_message)

#     return render_template('index.html', success=False)


# if __name__ == '__main__':
#     app.run(debug=True)


# ----------------------------------------------------------------------------------\

# from flask import Flask, render_template, request, redirect, url_for, send_file
# import os
# import pandas as pd
# from linkedin_api import Linkedin
# from urllib.parse import urlparse
# import json
# import logging
# from urllib.parse import unquote
# app = Flask(__name__)

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# ALLOWED_EXTENSIONS = {'xlsx'}


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def extract_company_name(linkedin_url):
#     parsed_url = urlparse((unquote(linkedin_url)))
#     path_segments = [
#         segment for segment in parsed_url.path.split('/') if segment]

#     if 'company' in path_segments:
#         company_index = path_segments.index('company')
#         if company_index < len(path_segments) - 1:
#             return path_segments[company_index + 1]

#     return None


# def fetch_company_details(api, company_name, linkedin_url):
#     try:
#         company_data = api.get_company(company_name)
#         return json.loads(json.dumps(company_data, indent=2))
#     except Exception as e:
#         logger.error(
#             f"Error fetching details for {company_name} from {linkedin_url}: {str(e)}")
#         return None


# def convert_to_billion_million(value):
#     if value is None:
#         return None

#     try:
#         value = float(value)
#     except (ValueError, TypeError):
#         return f"{value}"

#     billion_threshold = 1_000_000_000
#     million_threshold = 1_000_000

#     if value >= billion_threshold:
#         return f"{value / billion_threshold:.2f}B"
#     elif value >= million_threshold:
#         return f"{value / million_threshold:.2f}M"
#     else:
#         return f"{value:.2f}"


# # def process_urls(api, linkedin_urls_df):
#     all_company_details = []

#     for _, row in linkedin_urls_df.iterrows():
#         linkedin_url = row['LinkedIn URL']
#         company_name = extract_company_name(linkedin_url)

#         if company_name:
#             company_data = fetch_company_details(
#                 api, company_name, linkedin_url)

#             if company_data:
#                 try:
#                     employee_range_start = company_data.get(
#                         'staffCountRange', {}).get('start')
#                     employee_range_end = company_data.get(
#                         'staffCountRange', {}).get('end')
#                     funds = company_data.get('fundingData', {}).get(
#                         'lastFundingRound', {}).get('moneyRaised', {}).get('amount', " ")
#                     converted_funds = convert_to_billion_million(funds)
#                     industry = company_data.get('companyIndustries', [{}])[
#                         0].get('localizedName')
#                     hq = company_data.get('headquarter', {}).get('country')
#                     specialities = company_data.get('specialities')
#                     mem = company_data.get('staffCount')
#                     des = company_data.get('description')
#                     founded = company_data.get('foundedOn', {}).get('year')

#                     company_details = {
#                         'Company name': company_name,
#                         'Company Domain': company_data.get("companyPageUrl"),
#                         'Founded': founded,
#                         'ECR_start': employee_range_start,
#                         'ECR_End': employee_range_end,
#                         'Associated_members': mem,
#                         'Industry': industry,
#                         'HQ': hq,
#                         'Funds': converted_funds,
#                         'Description': des,
#                         'Specialities': specialities
#                     }

#                     all_company_details.append(company_details)
#                 except Exception as e:
#                     logger.error(
#                         f"Error extracting details for {company_name} from {linkedin_url}: {str(e)}")
#             else:
#                 logger.warning(
#                     f"No data fetched for {company_name} from {linkedin_url}.")

#     return pd.DataFrame(all_company_details)


# def process_urls(api, linkedin_urls_df):
#     all_company_details = []

#     for _, row in linkedin_urls_df.iterrows():
#         linkedin_url = row['LinkedIn URL']
#         company_name = extract_company_name(linkedin_url)
#         if company_name:
#             try:
#                 company_data = fetch_company_details(
#                     api, company_name, linkedin_url)

#                 if company_data:
#                     employee_range_start = company_data.get(
#                         'staffCountRange', {}).get('start')
#                     employee_range_end = company_data.get(
#                         'staffCountRange', {}).get('end')
#                     funds = company_data.get('fundingData', {}).get(
#                         'lastFundingRound', {}).get('moneyRaised', {}).get('amount', " ")
#                     converted_funds = convert_to_billion_million(funds)
#                     industry = company_data.get('companyIndustries', [{}])[
#                         0].get('localizedName')
#                     hq = company_data.get('headquarter', {}).get('country')
#                     specialities = company_data.get('specialities')
#                     mem = company_data.get('staffCount')
#                     des = company_data.get('description')
#                     founded = company_data.get('foundedOn', {}).get('year')

#                     company_details = {
#                         "Linkedin URL": linkedin_url,
#                         'Company name': company_name,
#                         'Company Domain': company_data.get("companyPageUrl"),
#                         'Founded': founded,
#                         'ECR_start': employee_range_start,
#                         'ECR_End': employee_range_end,
#                         'Associated_members': mem,
#                         'Industry': industry,
#                         'HQ': hq,
#                         'Funds': converted_funds,
#                         'Description': des,
#                         'Specialities': specialities
#                     }

#                     all_company_details.append(company_details)
#                 else:
#                     logger.warning(
#                         f"No data fetched for {company_name} from {linkedin_url}.")
#                     company_details = {
#                         "Linkedin URL": linkedin_url,
#                         'Company name': "",
#                         'Company Domain': "",
#                         'Founded': "",
#                         'ECR_start': "",
#                         'ECR_End': "",
#                         'Associated_members': "",
#                         'Industry': "",
#                         'HQ': "",
#                         'Funds': "",
#                         'Description': "",
#                         'Specialities': ""
#                     }
#                     all_company_details.append(company_details)
#             except Exception as e:
#                 logger.warning(f"Error processing {linkedin_url}: {str(e)}")
#                 company_details = {
#                     "Linkedin URL": linkedin_url,
#                     'Company name': "",
#                     'Company Domain': "",
#                     'Founded': "",
#                     'ECR_start': "",
#                     'ECR_End': "",
#                     'Associated_members': "",
#                     'Industry': "",
#                     'HQ': "",
#                     'Funds': "",
#                     'Description': "",
#                     'Specialities': ""
#                 }
#                 all_company_details.append(company_details)
#                 # If there's an error, add an empty row
#         else:
#             logger.warning(f"Invalid LinkedIn URL: {linkedin_url}")
#             # If the URL is invalid, add an empty row
#             company_details = {
#                 "Linkedin URL": linkedin_url,
#                 'Company name': "",
#                 'Company Domain': "",
#                 'Founded': "",
#                 'ECR_start': "",
#                 'ECR_End': "",
#                 'Associated_members': "",
#                 'Industry': "",
#                 'HQ': "",
#                 'Funds': "",
#                 'Description': "",
#                 'Specialities': ""
#             }
#             all_company_details.append(company_details)

#     return pd.DataFrame(all_company_details)


# processing = False


# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     return send_file(filename, as_attachment=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global processing  # Use the global variable

#     if request.method == 'POST':
#         processing = True  # Set processing to True when processing starts

#         file = request.files['file']

#         if file.filename == '':
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             filename = 'urls.xlsx'
#             file.save(filename)

#             linkedin_email = request.form['email']
#             linkedin_password = request.form['password']

#             if not linkedin_password:
#                 processing = False  # Set processing back to False if password is empty
#                 return render_template('index.html', error='Password cannot be empty.')

#             try:
#                 api = Linkedin(linkedin_email, linkedin_password)

#                 linkedin_urls_df = pd.read_excel(filename)
#                 processed_data = process_urls(api, linkedin_urls_df)

#                 output_filename = 'companies_data_with_details.xlsx'
#                 processed_data.to_excel(output_filename, index=False)

#                 processing = False  # Set processing back to False when processing is complete

#                 return render_template('index.html', success=True, output_filename=output_filename)
#             except Exception as e:
#                 processing = False  # Set processing back to False if an error occurs
#                 error_message = f"Error: {str(e)}"

#                 logger.error(error_message)
#                 return render_template('index.html', error=error_message)

#     return render_template('index.html', success=False, processing=processing)


# if __name__ == '__main__':
#     app.run(debug=True)

# ------------------------------------------------------------------------------------------------------------------
# will add rows if url is wrong

from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import pandas as pd
from linkedin_api import Linkedin
from urllib.parse import urlparse, unquote
import json
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_company_name(linkedin_url):
    parsed_url = urlparse(unquote(linkedin_url))
    path_segments = [
        segment for segment in parsed_url.path.split('/') if segment]

    if 'company' in path_segments:
        company_index = path_segments.index('company')
        if company_index < len(path_segments) - 1:
            return path_segments[company_index + 1]
    elif 'school' in path_segments:
        company_index = path_segments.index('school')
        if company_index < len(path_segments) - 1:
            return path_segments[company_index + 1]
    return None


def fetch_company_details(api, company_name, linkedin_url):
    try:
        company_data = api.get_company(company_name)
        return json.loads(json.dumps(company_data, indent=2))
    except Exception as e:
        logger.error(
            f"Error fetching details for {company_name} from {linkedin_url}: {str(e)}")
        return None


def convert_to_billion_million(value):
    if value is None:
        return None

    try:
        value = float(value)
    except (ValueError, TypeError):
        return f"{value}"

    billion_threshold = 1_000_000_000
    million_threshold = 1_000_000

    if value >= billion_threshold:
        return f"{value / billion_threshold:.2f}B"
    elif value >= million_threshold:
        return f"{value / million_threshold:.2f}M"
    else:
        return f"{value:.2f}"


def process_urls(api, linkedin_urls_df):
    all_company_details = []

    for _, row in linkedin_urls_df.iterrows():
        # record_id = row['Record ID']
        linkedin_url = row['LinkedIn URL']
        company_name = extract_company_name(linkedin_url)
        if company_name:
            try:
                company_data = fetch_company_details(
                    api, company_name, linkedin_url)

                if company_data:
                    employee_range_start = company_data.get(
                        'staffCountRange', {}).get('start')
                    employee_range_end = company_data.get(
                        'staffCountRange', {}).get('end')
                    funds = company_data.get('fundingData', {}).get(
                        'lastFundingRound', {}).get('moneyRaised', {}).get('amount', " ")
                    converted_funds = convert_to_billion_million(funds)
                    industry = company_data.get('companyIndustries', [{}])[
                        0].get('localizedName')
                    hq = company_data.get('headquarter', {}).get('country')
                    city = company_data.get('headquarter', {}).get('city')
                    specialities = company_data.get('specialities')
                    mem = company_data.get('staffCount')
                    des = company_data.get('description')
                    founded = company_data.get('foundedOn', {}).get('year')

                    company_details = {
                        # "Record ID": record_id,
                        "Linkedin URL": linkedin_url,
                        'Company name': company_name,
                        'Company Domain': company_data.get("companyPageUrl"),
                        'Founded': founded,
                        'ECR_start': employee_range_start,
                        'ECR_End': employee_range_end,
                        'Associated_members': mem,
                        'Industry': industry,
                        'HQ': hq,
                        'City':city,
                        'Funds': converted_funds,
                        'Description': des,
                        'Specialities': specialities
                    }

                    all_company_details.append(company_details)
                else:
                    logger.warning(
                        f"No data fetched for {company_name} from {linkedin_url}.")
                    company_details = {
                        # "Record ID": record_id,
                        "Linkedin URL": linkedin_url,
                        'Company name': "",
                        'Company Domain': "",
                        'Founded': "",
                        'ECR_start': "",
                        'ECR_End': "",
                        'Associated_members': "",
                        'Industry': "",
                        'HQ': "",
                        'City':"",
                        'Funds': "",
                        'Description': "",
                        'Specialities': ""
                    }
                    all_company_details.append(company_details)
            except Exception as e:
                logger.warning(f"Error processing {linkedin_url}: {str(e)}")
                company_details = {
                    # "Record ID": record_id,
                    "Linkedin URL": linkedin_url,
                    'Company name': "",
                    'Company Domain': "",
                    'Founded': "",
                    'ECR_start': "",
                    'ECR_End': "",
                    'Associated_members': "",
                    'Industry': "",
                    'HQ': "",
                    'City':"",
                    'Funds': "",
                    'Description': "",
                    'Specialities': ""
                }
                all_company_details.append(company_details)
        else:
            logger.warning(f"Invalid LinkedIn URL: {linkedin_url}")
            company_details = {
                # "Record ID": record_id,
                "Linkedin URL": linkedin_url,
                'Company name': "",
                'Company Domain': "",
                'Founded': "",
                'ECR_start': "",
                'ECR_End': "",
                'Associated_members': "",
                'Industry': "",
                'HQ': "",
                'City':"",
                'Funds': "",
                'Description': "",
                'Specialities': ""
            }
            all_company_details.append(company_details)

    return pd.DataFrame(all_company_details)


processing = False


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    global processing

    if request.method == 'POST':
        processing = True

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'urls.xlsx'
            file.save(filename)

            linkedin_email = request.form['email']
            linkedin_password = request.form['password']

            if not linkedin_password:
                processing = False
                return render_template('index.html', error='Password cannot be empty.')

            try:
                api = Linkedin(linkedin_email, linkedin_password)

                linkedin_urls_df = pd.read_excel(filename)
                processed_data = process_urls(api, linkedin_urls_df)

                output_filename = 'companies_data_with_details.xlsx'
                processed_data.to_excel(output_filename, index=False)

                processing = False
                return render_template('index.html', success=True, output_filename=output_filename)
            except Exception as e:
                processing = False
                error_message = f"Error: {str(e)}"

                logger.error(error_message)
                return render_template('index.html', error=error_message)

    return render_template('index.html', success=False, processing=processing)


if __name__ == '__main__':
    app.run(debug=False)
