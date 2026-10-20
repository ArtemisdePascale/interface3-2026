import requests
from icecream import ic
from tqdm import tqdm
import json
import os 

ic.configureOutput(includeContext=True)

COOKIES = {
    '_gcl_au': '1.1.1008619948.1792483676',
    '_ga': 'GA1.1.1834048030.1792483676',
    '_ga_5TBG2FXEXX': 'GS2.1.s1792483675$o1$g1$t1792483774$j55$l0$h0',
    '_shopify_essential': ':AaFYW9QLAAEAPGNyaUNbRngLkGBFPhq5QJxQJTutKuEdUh1E1jBw72DoHliu8piK8utrZ3RQWx3t7o-uLtEUJWMu7uA:',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'application/json',
    'Referer': 'https://shop.paperblanks.com/checkouts/cn/hWNIBJwqdIXGGZzB96VyroSv/en-be?_r=AQABVVnjhlXsuj7-DbUnvlq2UmOKo34bHHNHUiBzc_Kg7jUkUaqv&_s=cc80ac52-f08c-4a47-9351-65ed1b7573c8&_y=4f97982c-6044-4fba-bd9f-4711763cf5e9&auto_redirect=false&edge_redirect=true&skip_shop_pay=true',
    'content-type': 'application/json',
    'shopify-checkout-client': 'checkout-web/1.0',
    'shopify-checkout-source': 'id="hWNIBJwqdIXGGZzB96VyroSv", type="cn"',
    'x-checkout-one-session-token': 'AAEBhUzjC8JasCxwDKY-qHvR_cDkXCEO5n3QKPypijA8BLJdS_OQYVI0A8QWXXsL9snCccRzKIBZ20h-kONbpaZttPNxX5WSMP3uXOGZiA8rabsBpbN4bAYgIDrH09jPRGz4GSC1SiXBCnUQSy2F8vS-I7bU0c4vkW32_klVBF4gz8cYYC3IVGwAWvoVyg7rJCNwErSNqxOC0Hnsf2vQlZwChWhFYmnaqEBtizjhIOtjCdkDSXE4PA',
    'x-checkout-web-build-id': 'a8b6f7b2826dd97f6f8cd03ad395dbdf0b3b4a96',
    'x-checkout-web-deploy-stage': 'production',
    'x-checkout-web-server-handling': 'fast',
    'x-checkout-web-server-rendering': 'yes',
    'x-checkout-web-source-id': 'hWNIBJwqdIXGGZzB96VyroSv',
    'Origin': 'https://shop.paperblanks.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

PARAMS = {
    'operationName': 'Proposal',
}

def json_creator(code):
    json_data = {
        'variables': {
            'sessionInput': {
                'sessionToken': 'AAEBhUzjC8JasCxwDKY-qHvR_cDkXCEO5n3QKPypijA8BLJdS_OQYVI0A8QWXXsL9snCccRzKIBZ20h-kONbpaZttPNxX5WSMP3uXOGZiA8rabsBpbN4bAYgIDrH09jPRGz4GSC1SiXBCnUQSy2F8vS-I7bU0c4vkW32_klVBF4gz8cYYC3IVGwAWvoVyg7rJCNwErSNqxOC0Hnsf2vQlZwChWhFYmnaqEBtizjhIOtjCdkDSXE4PA',
            },
            'queueToken': 'A2Rcli7EVZkzHWBQrqxd3UIbloLiGjATxKwSJv0QRGK_-GXgX40CqZocRBaT8-p5r421QFEqgHrWEOqD4JWdEtfvhXN209bSzRTbGC7icS7YK4KpOxhOlqbWUT_jDyl_9w==',
            'discounts': {
                'lines': [],
                'acceptUnexpectedDiscounts': True,
            },
            'delivery': {
                'deliveryLines': [
                    {
                        'destination': {
                            'partialStreetAddress': {
                                'address1': '',
                                'city': '',
                                'countryCode': 'BE',
                                'lastName': '',
                                'phone': '',
                                'oneTimeUse': False,
                            },
                        },
                        'selectedDeliveryStrategy': {
                            'deliveryStrategyMatchingConditions': {
                                'estimatedTimeInTransit': {
                                    'any': True,
                                },
                                'shipments': {
                                    'any': True,
                                },
                            },
                            'options': {},
                        },
                        'targetMerchandiseLines': {
                            'any': True,
                        },
                        'deliveryMethodTypes': [
                            'SHIPPING',
                        ],
                        'expectedTotalPrice': {
                            'any': True,
                        },
                        'destinationChanged': True,
                    },
                ],
                'noDeliveryRequired': [],
                'useProgressiveRates': False,
                'prefetchShippingRatesStrategy': None,
                'supportsSplitShipping': True,
            },
            'deliveryExpectations': {
                'deliveryExpectationLines': [],
            },
            'merchandise': {
                'merchandiseLines': [
                    {
                        'stableId': '030d4e54-6ebb-4c38-9ad3-1d7849cef8de',
                        'merchandise': {
                            'productVariantReference': {
                                'id': 'gid://shopify/ProductVariantMerchandise/43169638908017',
                                'variantId': 'gid://shopify/ProductVariant/43169638908017',
                                'properties': [],
                                'sellingPlanId': None,
                                'sellingPlanDigest': None,
                            },
                        },
                        'quantity': {
                            'items': {
                                'value': 1,
                            },
                        },
                        'expectedTotalPrice': {
                            'value': {
                                'amount': '20.95',
                                'currencyCode': 'EUR',
                            },
                        },
                        'lineComponentsSource': None,
                        'lineComponents': [],
                    },
                ],
            },
            'memberships': {
                'memberships': [],
            },
            'payment': {
                'totalAmount': {
                    'any': True,
                },
                'paymentLines': [
                    {
                        'paymentMethod': {
                            'directPaymentMethod': None,
                            'giftCardPaymentMethod': None,
                            'ownedGiftCardPaymentMethod': None,
                            'redeemablePaymentMethod': None,
                            'walletPaymentMethod': None,
                            'walletsPlatformPaymentMethod': None,
                            'localPaymentMethod': None,
                            'paymentOnDeliveryMethod': None,
                            'paymentOnDeliveryMethod2': None,
                            'manualPaymentMethod': None,
                            'customPaymentMethod': None,
                            'offsitePaymentMethod': None,
                            'customOnsitePaymentMethod': {
                                'name': 'Bancontact',
                                'paymentMethodIdentifier': '15055900dcf7b3d42ea34f23acf16875',
                                'billingAddress': {
                                    'streetAddress': {
                                        'address1': '',
                                        'city': '',
                                        'countryCode': 'BE',
                                        'lastName': '',
                                        'phone': '',
                                    },
                                },
                                'paymentAttributes': '',
                            },
                            'deferredPaymentMethod': None,
                            'customerCreditCardPaymentMethod': None,
                            'paypalBillingAgreementPaymentMethod': None,
                            'remotePaymentInstrument': None,
                        },
                        'amount': {
                            'any': True,
                        },
                    },
                ],
                'billingAddress': {
                    'streetAddress': {
                        'address1': '',
                        'city': '',
                        'countryCode': 'BE',
                        'lastName': '',
                        'phone': '',
                    },
                },
                'allowStoreCredit': False,
            },
            'buyerIdentity': {
                'customer': {
                    'presentmentCurrency': 'EUR',
                    'countryCode': 'BE',
                },
                'phoneCountryCode': 'BE',
                'marketingConsent': [
                    {
                        'email': {
                            'consentState': 'DECLINED',
                        },
                    },
                ],
                'shopPayOptInPhone': {
                    'countryCode': 'BE',
                },
                'rememberMe': False,
            },
            'tip': {
                'tipLines': [],
            },
            'taxes': {
                'proposedAllocations': None,
                'proposedTotalAmount': None,
                'proposedTotalIncludedAmount': {
                    'value': {
                        'amount': '3.64',
                        'currencyCode': 'EUR',
                    },
                },
                'proposedMixedStateTotalAmount': None,
                'proposedExemptions': [],
            },
            'note': {
                'message': None,
                'customAttributes': [
                    {
                        'key': 'pb_cart_id',
                        'value': '46f8bdaf-bc07-419a-ba1b-a950d9ee6d54',
                    },
                ],
            },
            'localizationExtension': {
                'fields': [],
            },
            'nonNegotiableTerms': None,
            'scriptFingertqdm.write': {
                'signature': None,
                'signatureUuid': None,
                'lineItemScriptChanges': [],
                'paymentScriptChanges': [],
                'shippingScriptChanges': [],
            },
            'optionalDuties': {
                'buyerRefusesDuties': False,
            },
            'reduction': {
                'code': code,
            },
            'cartMetafields': [],
        },
        'operationName': 'Proposal',
        'id': '3ab783e53b0ef16d807e2dcfc37f03217b23de0f710307e5da9069361cd94453',
    }

    return json_data

def main():
    with open('fuzzcoupons.txt') as fp:
        lines = fp.read().splitlines()
    promocodes = [l.strip() for l in lines]

    if os.path.isfile('output/shop.paperblanks.com.json'):
        with open('output/shop.paperblanks.com.json') as fp:
            stored = json.load(fp)
    else:
        stored = {}

    for promo in tqdm(promocodes):
        try:
            if promo in stored:
                if stored[promo].get("works", False):
                    tqdm.write(f"{promo} WORKS ({stored[promo].get('value', 'unknown')} off)")
            
                continue
            
                    
            reduction = 'unknown'

            response = requests.post(
                'https://shop.paperblanks.com/checkouts/internal/graphql/persisted',
                params=PARAMS,
                cookies=COOKIES,
                headers=HEADERS,
                json=json_creator(promo),
            )
            res = response.json()

            errors = res['data']['session']['negotiate']['errors']
            result = res['data']['session']['negotiate']['result']
            if any(err['code'] == 'REDUCTION_INVALID_CODE' for err in errors):
                stored[promo] = {
                    "works": False,
                    "value": 'unknown'
                }
                tqdm.write(f"{promo} did not work")
                continue
            else:
                for line in result['sellerProposal']['merchandiseDiscount']['lines']:
                    if line['__typename'] == 'DiscountLine':
                        discount = line['discount']['value']
                        if discount['__typename'] == 'PercentageValue':
                            reduction = f"{discount['percentage']}%"
                        else:
                            ic(discount)

                stored[promo] = {
                    "works": True,
                    "value": reduction
                }
                tqdm.write(f"{promo} WORKS ({reduction} off)")

            continue
        except Exception as e:
            ic(e)
            break
    
    with open('output/shop.paperblanks.com.json', 'w') as fp:
        json.dump(stored, fp)



if __name__ == "__main__":
    main()