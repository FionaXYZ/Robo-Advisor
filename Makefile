DATAOUT="quotes.jl"
LOGOUT="scrap.log"

.PHONY: clean

scrap: clean
	scrapy runspider web.py -O $(DATAOUT) --logfile=$(LOGOUT)

clean:
	rm  -f $(DATAOUT)