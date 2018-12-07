from scrapy import Spider
from scrapy.http import Request
import pyexcel,csv
import pdb

def product_info(response, value):
    return response.xpath('//th[contains(text(),"'+ value +'")]/following-sibling::td/text()').extract_first()

def product_ainfo(response, value):
    return response.xpath('//th[contains(text(),"'+ value +'")]/following-sibling::td/a/text()').extract_first()

def product_linfo(response,value):
    return response.xpath('//th[contains(text(),"'+ value +'")]/following-sibling::td/a/text()').extract()

class SubjectsSpider(Spider):
    name = 'movies'
    allowed_domains = ['www.amazon.de']
    start_urls = ['https://www.amazon.de/s/ref=sr_pg_1?rh=n%3A3010075031%2Cp_85%3A3282148031%2Cp_n_entity_type%3A9739119031%2Cp_n_ways_to_watch%3A7448693031&bbn=3010075031&ie=UTF8&qid=1543982101']
    
    # outfile = open("output.csv", "w", newline="")
    # writer = csv.writer(outfile)

    def parse(self, response):
        urls=response.xpath('//*[contains(@class,"s-access-detail-page")]/@href').extract()
        for url in urls:            
            yield Request(url, callback=self.parse_details)
            #yield {'urls':url}
            
        next_page_url=response.xpath('//*[contains(@class,"pagnNext")]/@href').extract_first()
        absolute_next_page_url=response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)
           
    def parse_details(self,response):
        title=response.xpath('//*[contains(@class,"av-detail-section")]//h1/text()').extract_first()
        #print(title)
        #duration=response.xpath('//*[contains(@class,"av-badge-text")][2]/text()').extract_first()
        duration=response.xpath('//span[contains(@data-automation-id,"runtime-badge")]/text()').extract_first()
        #duration=response.xpath('//section[contains(@class,"av-detail-section")]//span[contains(@data-automation-id,"runtime-badge")]/text()').extract_first()
        print('d',duration)
        ratings=response.xpath('//*[contains(@href,"#customer-review-section")]/span/@class').extract_first()
        released_year=response.xpath('//*[contains(@data-automation-id,"release-year-badge")]/text()').extract_first()
        details=response.xpath('//*[contains(@data-automation-id,"synopsis")]/div/div/text()').extract_first()
        rent_HD=response.xpath('//button[@data-quality="HD" and ./span/text()="Kaufen in "]/@data-purchasing-modal-text').extract_first()
        # print(rent_HD)
        rent_SD=response.xpath('//button[@data-quality="SD" and ./span/text()="Kaufen in "]/@data-purchasing-modal-text').extract_first()
        buy_HD=response.xpath('//button[@data-quality="HD" and ./span/text()="Ausleihen in "]/@data-purchasing-modal-text').extract_first()
        buy_SD=response.xpath('//button[@data-quality="SD" and ./span/text()="Ausleihen in "]/@data-purchasing-modal-text').extract_first()

        # rent=response.xpath('//button/@data-purchasing-modal-text').extract_first()
        # try:
        #     buy=response.xpath('//button/@data-purchasing-modal-text')[1].extract()
        # except:
        #     pass
        # genre=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[1]/td/a/text()').extract()
        # direction=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[2]/td/a/text()').extract()
        # main_actors=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[3]/td/a/text()').extract()
        # Supporting_Actor=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[4]/td/a/text()').extract()
        # Studio=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[5]/td/text()').extract_first()
        # FSK_Review=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[6]/td/text()').extract_first()
        # producers=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[7]/td/a/text()').extract_first()
        # languages=response.xpath('//table[contains(@class,"a-align-top product-details-meta")]/tr[8]/td/text()').extract_first()
        genre=product_ainfo(response,'Genre')
        direction=product_linfo(response,'Regie')
        main_actors=product_linfo(response,'Hauptdarsteller')
        Supporting_Actor=product_linfo(response,'Nebendarsteller')
        Studio=product_info(response,'Studio')
        FSK_Review=product_info(response,'Bewertung')
        producers=product_ainfo(response,'Produzenten')
        languages=product_info(response,'Sprachen')
        subtitle=product_info(response,'Untertitel')
        

        def string_clean(response,value):
            try:
                rn=value.replace("\n","")
                cleaned=' '.join(rn.split())                         
                return cleaned
            except:
                pass

        def get_duration(response,value):           
            # if value:
            #     duration=value.replace("Std.","Hours")
            #     return duration
            # print(value)
            if value:
                d=[int(s) for s in value.split() if s.isdigit()]
                try:
                    minutes=d[0]*60+d[1]
                except IndexError:
                    minutes=d[0]*60
            else:
                return None
            return minutes


        # def get_numbers(response,value):
        #     numb=[s for s in list(ratings) if s.isdigit()]
        #     return numb

        def put_point(response,value):
            #rt=get_numbers(response,value)
            if value:
                rt=[s for s in list(value) if s.isdigit()]
                rt="".join(rt)
                point=rt[:1]+"."+rt[1:]
                return point     
            else:
                pass

        
        # data=[['Title','Duration','Ratings','Released_Year','Details','Rent(EUR)','Buy(EUR)'],[title,get_duration(response,duration),put_point(response,ratings),released_year,details,put_point(response,rent),put_point(response,buy)]]
        # yield pyexcel.save_as(array = data, dest_file_name = 'csv_file_name.csv')

        # self.writer.writerow([title,get_duration(response,duration),put_point(response,ratings),released_year,details,put_point(response,rent),put_point(response,buy),genre,direction,main_actors])
        yield{
            'title':title,
            'duration':get_duration(response,duration),           
            'released_year':released_year,
            'synopsis':details,
            'rent_HD(EUR)':put_point(response,rent_HD),
            'buy_HD(EUR)':put_point(response,buy_HD),
            'rent_SD(EUR)':put_point(response,rent_SD),
            'buy_SD(EUR)':put_point(response,buy_SD),
            'genre':genre,
            'direction':direction,
            'cast':main_actors + Supporting_Actor,
            'Studio':string_clean(response,Studio),
            'FSK_Review':string_clean(response,FSK_Review),           
            'languages':string_clean(response,languages),
            # 'ratings':put_point(response,ratings),
            # 'producers':producers,
            # 'subtitles':string_clean(response,subtitle)
        }

        # def close(self):
        #     self.outfile.close()
        #     print("-----Check to see if this is closed-----")
