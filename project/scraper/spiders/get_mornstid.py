import scrapy
import html 
from scrapy.selector import Selector

#step 1
#getting morningstar number to search for encrypted website url
#going through the websites in web.py

class QuotesSpider(scrapy.Spider):
    name = 'mornst_id'


    def start_requests(self):
        for ISIN in self.settings['PROJ_USERINPUT_ISINS']:
            yield scrapy.FormRequest(
                f'https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?page=1&pageSize=10&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL&securityDataPoints=SecId%7CName%7CPriceCurrency%7CTenforeId%7CLegalName%7CClosePrice%7CStarRatingM255%7CSustainabilityRank%7CQuantitativeRating%7CAnalystRatingScale%7CCategoryName%7CYield_M12%7CGBRReturnD1%7CGBRReturnW1%7CGBRReturnM1%7CGBRReturnM3%7CGBRReturnM6%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CMaxFrontEndLoad%7COngoingCostActual%7CPerformanceFeeActual%7CTransactionFeeActual%7CMaximumExitCostAcquired%7CFeeLevel%7CManagerTenure%7CMaxDeferredLoad%7CInitialPurchase%7CFundTNAV%7CEquityStyleBox%7CBondStyleBox%7CAverageMarketCapital%7CAverageCreditQualityCode%7CEffectiveDuration%7CMorningstarRiskM255%7CAlphaM36%7CBetaM36%7CR2M36%7CStandardDeviationM36%7CSharpeM36%7CInvestorTypeRetail%7CInvestorTypeProfessional%7CInvestorTypeEligibleCounterparty%7CExpertiseBasic%7CExpertiseAdvanced%7CExpertiseInformed%7CReturnProfilePreservation%7CReturnProfileGrowth%7CReturnProfileIncome%7CReturnProfileHedging%7CReturnProfileOther%7CTrackRecordExtension&filters=&term={ISIN}&subUniverseId=',
                callback=self.parse_mornstid
            )

    def parse_mornstid(self, response):

        str = response.json()['rows']
        morn_id=str[0]['SecId']
        isin=str[0]['TenforeId'].split('.')[-1]

        yield {  
                'ISIN':isin,
                'mornst_id':morn_id
        }




