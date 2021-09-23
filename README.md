# web_crawler
實作網路爬蟲
## Xpath
一般會使用lxml.etree將網頁的html轉換成樹狀結構，該樹每個節點相當於html的元素，

再使用Xpath語法來抓取特定節點的內容，下圖為agoda訂房網站的html範例。

![html_example](/image/html_example.png "html_example")

可以觀察到飯店名稱美亞商旅，位於擁有屬性data-selenium且其值為"hotel-name"的h3標籤中，

可以透過下列Xpath指令來得到對應的值，該指令會找到所有擁有屬性data-selenium且其值為"hotel-name"的h3標籤的文字內容。

```
//h3[@data-selenium="hotel-name"]//text()
```

## et_crawler
爬取ettody新聞雲的即時新聞，並儲存新聞報導時間、標題、新聞內容與新聞的超連結。

網站頁面

![ettoday新聞雲即時新聞](/image/et_page.png "ettoday新聞雲即時新聞")

爬取結果

![ettoday新聞雲爬取結果](/image/et_result.png "ettoday新聞雲爬取結果")
## agoda_crawler
爬取agoda訂房網站的飯店資訊，儲存飯店名稱、星級、設備、優惠與價格等資訊。

網站頁面

![agoda訂房資訊](/image/agoda_page.png "agoda訂房資訊")

爬取結果

![agoda訂房資訊爬取結果](/image/agoda_result.png "agoda訂房資訊爬取結果")
