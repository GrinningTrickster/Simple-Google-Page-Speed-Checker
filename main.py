import pandas as pd
import urllib
import requests
import json
from datetime import datetime
from urllib.parse import urlparse

# key for page speed api
key = 'INSERT KEY'

service_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed/"

date = datetime.today().strftime('%Y-%m-%d')

lab_headers = ('URL', 'Date', 'Score', 'FCP', 'Speed Index', 'LCP', 'Interactive', 'TBT', 'CLS')
field_headers = ('URL', 'Date', 'Overall Score', 'FCP Percentile', 'FCP Category', 'LCP Percentile', 'LCP Category',
                 'FID Percentile', 'FID Category', 'CLS Percentile', 'CLS Category')


def speed_test_url(url, device):
    params = {
        "?url": url,
        'strategy': device,
        'key': key,
    }
    data = urllib.parse.urlencode(params, doseq=True)
    main_call = urllib.parse.urljoin(service_url, data)
    main_call = main_call.replace(r'%3F', r'?')
    response = requests.get(main_call).json()

    # lab data
    try:
        score = response['lighthouseResult']['categories']['performance']['score']
    except:
        score = 0.0

    try:
        fcp = response['lighthouseResult']['audits']['first-contentful-paint']['score']
    except:
        fcp = 0.0

    try:
        si = response['lighthouseResult']['audits']['speed-index']['score']
    except:
        si = 0.0

    try:
        lcp = response['lighthouseResult']['audits']['largest-contentful-paint']['score']
    except:
        lcp = 0.0

    try:
        interactive = response['lighthouseResult']['audits']['interactive']['score']
    except:
        interactive = 0.0

    try:
        tbt = response['lighthouseResult']['audits']['total-blocking-time']['score']
    except:
        tbt = 0.0

    try:
        cls = response['lighthouseResult']['audits']['cumulative-layout-shift']['score']
    except:
        cls = 0.0

    # origin check (prevent defaulting to origin information when requesting field)

    try:
        origin_pass = response['loadingExperience']['origin_fallback']
    except:
        origin_pass = False


    # field data
    if origin_pass == False:
        try:
            field_pass_fail = response['loadingExperience']['overall_category']
        except:
            field_pass_fail = 'unavailable'

        try:
            field_fcp_percentile = response['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile']
        except:
            field_fcp_percentile = 0.0

        try:
            field_fcp_category = response['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']
        except:
            field_fcp_category = ''

        try:
            field_lcp_percentile = response['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile']
            field_lcp_percentile = field_lcp_percentile/1000
        except:
            field_lcp_percentile = 0.0

        try:
            field_lcp_category = response['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['category']
        except:
            field_lcp_category = ''

        try:
            field_fid_percentile = response['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
        except:
            field_fid_percentile = 0.0

        try:
            field_fid_category = response['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category']
        except:
            field_fid_category = ''

        try:
            field_cls_percentile = response['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['percentile']
            field_cls_percentile = field_cls_percentile/100
        except:
            field_cls_percentile = 0.0

        try:
            field_cls_category = response['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['category']
        except:
            field_cls_category = ''
    else:
        field_pass_fail = 'unavailable'
        field_fcp_percentile = 0.0
        field_fcp_category = ''
        field_lcp_percentile = 0.0
        field_lcp_category = ''
        field_fid_percentile = 0.0
        field_fid_category = ''
        field_cls_percentile = 0.0
        field_cls_category = ''

    # origin data

    try:
        ofield_pass_fail = response['originLoadingExperience']['overall_category']
    except:
        ofield_pass_fail  = ''

    try:
        ofield_fcp_percentile = response['originLoadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS'][
            'percentile']
    except:
        ofield_fcp_percentile = 0.0

    try:
        ofield_fcp_category = response['originLoadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']
    except:
        ofield_fcp_category = ''

    try:
        ofield_lcp_percentile = response['originLoadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS'][
            'percentile']
        ofield_lcp_percentile = ofield_lcp_percentile/1000
    except:
        ofield_lcp_percentile = 0.0

    try:
        ofield_lcp_category = response['originLoadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['category']
    except:
        ofield_lcp_category = ''

    try:
        ofield_fid_percentile = response['originLoadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
    except:
        ofield_fid_percentile = 0.0

    try:
        ofield_fid_category = response['originLoadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category']
    except:
        ofield_fid_category = ''

    try:
        ofield_cls_percentile = response['originLoadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE'][
            'percentile']
        ofield_cls_percentile = ofield_cls_percentile/100
    except:
        ofield_cls_percentile = 0.0

    try:
        ofield_cls_category = response['originLoadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE'][
            'category']
    except:
        ofield_cls_category = ''

    lab_result = (url, date, score, fcp, si, lcp, interactive, tbt, cls)

    field_result = (url, date, field_pass_fail, field_fcp_percentile, field_fcp_category, field_lcp_percentile, field_lcp_category,
                   field_fid_percentile, field_fid_category, field_cls_percentile, field_cls_category)

    ofield_result = (url, date, ofield_pass_fail, ofield_fcp_percentile, ofield_fcp_category, ofield_lcp_percentile,
                    ofield_lcp_category, ofield_fid_percentile, ofield_fid_category, ofield_cls_percentile,
                    ofield_cls_category)

    with open('result.json', 'w') as outfile:
        json.dump(response, outfile, indent=4)

    return lab_result, field_result, ofield_result


if __name__ == '__main__':

    speed_file = 'speed-urls.txt'

    with open(speed_file) as h:
        speed_urls = h.readlines()
    speed_urls = [x.strip() for x in speed_urls]

    # acquires domain/search console account
    origin_list = set([])
    for url in speed_urls:
        try:
            full_url = urlparse(url)
            origin_url = str(full_url.scheme + "://" + full_url.hostname + "/")
            origin_list.add(origin_url)
        except:
            continue

    originMobileList = []
    originDesktopList = []
    for url in origin_list:
        try:
            print(url)
            olab_speed_metrics, ofield_speed_metrics, origin_results = speed_test_url(url, device='mobile')
            originMobileList.append(origin_results)
            olab_desktop_speed_metrics, ofield_desktop_speed_metrics, origin_dsk_results \
                = speed_test_url(url, device='desktop')
            originDesktopList.append(origin_dsk_results)
        except:
            continue

    labMobileList = []
    fieldMobileList = []
    for url in speed_urls:
        try:
            print(url)
            lab_speed_metrics, field_speed_metrics, ofield_results = speed_test_url(url, device='mobile')
            labMobileList.append(lab_speed_metrics)
            fieldMobileList.append(field_speed_metrics)
        except:
            continue


    labDesktopList = []
    fieldDesktopList = []
    for url in speed_urls:
        try:
            print(url)
            lab_desktop_speed_metrics, field_desktop_speed_metrics, ofield_dsk_results = speed_test_url(
                url, device='desktop')
            labDesktopList.append(lab_desktop_speed_metrics)
            fieldDesktopList.append(field_desktop_speed_metrics)
        except:
            continue

    dfOriginMobile = pd.DataFrame(originMobileList)
    dfOriginDesktop = pd.DataFrame(originDesktopList)
    dfLabMobile = pd.DataFrame(labMobileList)
    dfLabDesktop = pd.DataFrame(labDesktopList)
    dfFieldMobile = pd.DataFrame(fieldMobileList)
    dfFieldDesktop = pd.DataFrame(fieldDesktopList)

    # origin mobile
    originMobileWriter = pd.ExcelWriter(date + '-origin-mobile-results.xlsx', engine='xlsxwriter')
    dfOriginMobile.to_excel(originMobileWriter, sheet_name='results', index=False, header=field_headers)
    originMobileWriter.save()

    # origin desktop
    originDesktopWriter = pd.ExcelWriter(date + '-origin-desktop-results.xlsx', engine='xlsxwriter')
    dfOriginDesktop.to_excel(originDesktopWriter, sheet_name='results', index=False, header=field_headers)
    originDesktopWriter.save()

    # lab mobile
    labMobileWriter = pd.ExcelWriter(date + '-lab-mobile-results.xlsx', engine='xlsxwriter')
    dfLabMobile.to_excel(labMobileWriter, sheet_name='results', index=False, header=lab_headers)
    labMobileWriter.save()

    #lab desktop
    labDesktopWriter = pd.ExcelWriter(date + '-lab-desktop-results.xlsx', engine='xlsxwriter')
    dfLabDesktop.to_excel(labDesktopWriter, sheet_name='results', index=False, header=lab_headers)
    labDesktopWriter.save()

    #field mobile
    mobileFieldWriter = pd.ExcelWriter(date + '-field-mobile-results.xlsx', engine='xlsxwriter')
    dfFieldMobile.to_excel(mobileFieldWriter, sheet_name='results', index=False, header=field_headers)
    mobileFieldWriter.save()

    #field desktop
    fieldDesktopWriter = pd.ExcelWriter(date + '-field-desktop-results.xlsx', engine='xlsxwriter')
    dfFieldDesktop.to_excel(fieldDesktopWriter, sheet_name='results', index=False, header=field_headers)
    fieldDesktopWriter.save()

