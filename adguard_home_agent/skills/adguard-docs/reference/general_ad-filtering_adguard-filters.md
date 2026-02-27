[Skip to main content](https://adguard.com/kb/general/ad-filtering/adguard-filters/#docusaurus_skipToContent_fallback)
[![AdGuard](https://adguard.com/kb/img/logo.svg)](https://adguard.com/kb/)[Docs](https://adguard.com/kb/)[Blog](https://adguard.com/blog/index.html)[Official website](https://adguard.com)
[](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
  * [English](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
  * [Русский](https://adguard.com/kb/ru/general/ad-filtering/adguard-filters/)
  * [Deutsch](https://adguard.com/kb/de/general/ad-filtering/adguard-filters/)
  * [Čeština](https://adguard.com/kb/cs/general/ad-filtering/adguard-filters/)
  * [Français](https://adguard.com/kb/fr/general/ad-filtering/adguard-filters/)
  * [Español](https://adguard.com/kb/es/general/ad-filtering/adguard-filters/)
  * [Italiano](https://adguard.com/kb/it/general/ad-filtering/adguard-filters/)
  * [Português (Brasil)](https://adguard.com/kb/pt-BR/general/ad-filtering/adguard-filters/)
  * [日本語](https://adguard.com/kb/ja/general/ad-filtering/adguard-filters/)
  * [한국어](https://adguard.com/kb/ko/general/ad-filtering/adguard-filters/)
  * [中文（中国）](https://adguard.com/kb/zh-CN/general/ad-filtering/adguard-filters/)
  * [中文（台灣）](https://adguard.com/kb/zh-TW/general/ad-filtering/adguard-filters/)
  * [Help Us Translate](https://adguard.com/kb/miscellaneous/contribute/translate/program/)


[GitHub](https://github.com/AdguardTeam/KnowledgeBase)
Search`K`
[![AdGuard](https://adguard.com/kb/img/logo.svg)](https://adguard.com/kb/)
  * [Overview](https://adguard.com/kb/)
  * [General](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
    * [Ad filtering](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
      * [How ad blocking works](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
      * [AdGuard filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
      * [Search ads and self-promotion](https://adguard.com/kb/general/ad-filtering/search-ads/)
      * [Tracking filter rules statistics](https://adguard.com/kb/general/ad-filtering/tracking-filter-statistics/)
      * [How to create your own ad filters](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
      * [AdGuard filter policy](https://adguard.com/kb/general/ad-filtering/filter-policy/)
    * [HTTPS filtering](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
    * [Phishing and malware protection](https://adguard.com/kb/general/browsing-security/)
    * [Tracking protection (formerly Stealth Mode)](https://adguard.com/kb/general/stealth-mode/)
    * [AdGuard account](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
    * [Extensions](https://adguard.com/kb/general/extensions/)
    * [License](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
    * [How to install AdGuard](https://adguard.com/kb/general/how-to-install/)
  * [AdGuard for Windows](https://adguard.com/kb/adguard-for-windows/)
  * [AdGuard for Windows v8](https://adguard.com/kb/adguard-for-windows-8/)
  * [AdGuard for Mac](https://adguard.com/kb/adguard-for-mac/)
  * [AdGuard for Android](https://adguard.com/kb/adguard-for-android/)
  * [AdGuard for iOS](https://adguard.com/kb/adguard-for-ios/)
  * [AdGuard Browser Extension](https://adguard.com/kb/adguard-browser-extension/)
  * [AdGuard for Safari](https://adguard.com/kb/adguard-for-safari/)
  * [AdGuard Mini for Mac](https://adguard.com/kb/adguard-mini-for-mac/)
  * [AdGuard Content Blocker](https://adguard.com/kb/adguard-content-blocker/)
  * [AdGuard for Linux](https://adguard.com/kb/adguard-for-linux/)
  * [Miscellaneous](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
  * [Guides](https://adguard.com/kb/general/ad-filtering/adguard-filters/)


  * [](https://adguard.com/kb/)
  * General
  * Ad filtering
  * AdGuard filters


On this page
# AdGuard filters
This article is about the filters that we develop and that come pre-installed in AdGuard. To check them out, you can [download the AdGuard app](https://agrd.io/download-kb-adblock)
This article is about the filters we create to use in AdGuard and other ad-blocking software (e.g., uBlock Origin). Filters are sets of rules in text format used by AdGuard apps and programs to filter out advertising and privacy-threatening content such as banners, popups, or trackers. Filters contain lists of rules based on their purpose. Language filters include rules for corresponding language segments of the Internet (e.g., German filter). Task-based filters group rules that fulfil a specific task, such as Social media filter or Tracking Protection filter. Enabling or disabling a filter makes it easier to work with the entire list of rules at once.
## AdGuard filters[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#adguard-filters "Direct link to heading")
  * **Base filter** removes ads from websites with English content. Originally based on [EasyList](https://easylist.to/) and modified by us. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt)
  * **Tracking Protection filter** — comprehensive list of various online counters and web analytics tools. Use it to hide your actions online and avoid tracking. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_3_Spyware/filter.txt)
  * **URL Tracking filter** enhances privacy by removing tracking parameters from URLs. When a user opts to block tracking parameters in Stealth Mode, this filter will be enabled automatically. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_17_TrackParam/filter.txt)
  * **Social media filter** removes numerous "Like" and "Tweet" buttons and other social media integrations on popular websites. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_4_Social/filter.txt)
  * **Annoyances filter** blocks irritating elements on web pages. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_14_Annoyances/filter.txt). Includes the following AdGuard filters (all of them can be enabled separately from the Annoyances filter):
    * **Cookie Notices** blocks cookie notices on web pages. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_18_Annoyances_Cookies/filter.txt)
    * **Popups** blocks all kinds of popups that are not necessary for websites' operation. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_19_Annoyances_Popups/filter.txt)
    * **Mobile App Banners** blocks banners that promote mobile apps of websites. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_20_Annoyances_MobileApp/filter.txt)
    * **Widgets** blocks third-party widgets: online assistants, live support chats, etc. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_22_Annoyances_Widgets/filter.txt)
    * **Other Annoyances** blocks elements that do not fall under the popular categories of annoyances. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_21_Annoyances_Other/filter.txt)
  * **Filter unblocking search ads and self-promotions** unblocks ads that may be useful to users. Learn more about this filter on [this page](https://adguard.com/kb/general/ad-filtering/search-ads/). [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_10_Useful/filter.txt)
  * **Russian filter** removes ads from websites in Russian. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_1_Russian/filter.txt)
  * **German filter** removes ads from websites in German. Originally based on the [EasyList Germany](https://easylist.to/) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt)
  * **French filter** removes ads from websites in French. Originally based on the [Liste FR](https://forums.lanik.us/viewforum.php?f=91) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_16_French/filter.txt)
  * **Japanese filter** removes ads from websites in Japanese. Originally based on the [Fanboy’s Japanese](https://www.fanboy.co.nz/fanboy-japanese.txt) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_7_Japanese/filter.txt)
  * **Dutch filter** removes ads from websites in Dutch. Originally based on the [EasyList Dutch](https://easylist.to/) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_8_Dutch/filter.txt)
  * **Spanish/Portuguese filter** removes ads from websites in Spanish and Portuguese. Originally based on the [Fanboy’s Spanish/Portuguese](https://www.fanboy.co.nz/fanboy-espanol.txt) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_9_Spanish/filter.txt)
  * **Turkish filter** removes ads from websites in Turkish. Created by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_13_Turkish/filter.txt)
  * **Chinese filter** removes ads from websites in Chinese. Originally based on the [EasyList China](https://github.com/easylist/easylistchina) filter and subsequently modified by us according to the complaints from users. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt)
  * **Ukrainian filter** removes ads from websites in Ukrainian. Learn more about this filter on [this page](https://adguard.com/en/blog/ukrainian-filter.html). [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_23_Ukrainian/filter.txt)
  * **Experimental filter** serves to test some new filtering rules that can potentially cause conflicts and mess with websites' work. In case these rules perform without any issues, they get added to main filters. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_5_Experimental/filter.txt)
  * **Mobile ads filter** blocks ads on mobile devices. Contains all known mobile ad networks. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt)
  * **DNS filter** — composed of several other filters (AdGuard Base filter, Social media filter, Spyware filter, Mobile ads filter, EasyList and EasyPrivacy) and simplified specifically to be better compatible with DNS-level ad blocking. This filter is used by [AdGuard DNS](https://adguard-dns.io/kb) servers to block ads and tracking. [View rules](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt)


## AdGuard Filters Policy[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#adguard-filters-policy "Direct link to heading")
Our filter policy defines what AdGuard filters should and shouldn't block, as well as the rules for adding and removing rules from filters. Read the full text of [AdGuard filter policy](https://adguard.com/kb/general/ad-filtering/filter-policy/) for detailed information.
## Contributing to AdGuard filters[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#contributing-to-adguard-filters "Direct link to heading")
We are blessed with a unique community that not only loves AdGuard but also gives back. Many people volunteer in various ways to make AdGuard's user experience better for everybody. You are welcome to join the band and make a difference. We will do our part and happily reward the most active community. So, what can you do?
### Report Issues[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#report-issues "Direct link to heading")
We rely on the community to let us know about issues with our filters. It helps us use our time more efficiently and keep filters constantly updated. To submit a report, please use this [web reporting tool](https://agrd.io/report).
### Suggest Filtering Rules[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#suggest-filtering-rules "Direct link to heading")
You will find many open issues in the [GitHub filter repository](https://github.com/AdguardTeam/AdguardFilters/issues). Each one refers to a problem with a website, such as a missed ad or a false positive. Pick an issue and suggest your own rules in the comments. AdGuard filter engineers will review your suggestions and, if approved, add your rules to AdGuard filters.
Here is the [official documentation](https://adguard.com/kb/general/ad-filtering/create-own-filters/) on the syntax of AdGuard filtering rules. Please read it carefully: it will help you create your own filtering rules.
### Other ways to contribute[​](https://adguard.com/kb/general/ad-filtering/adguard-filters/#other-ways-to-contribute "Direct link to heading")
Here is [a dedicated page](https://adguard.com/contribute.html) for people willing to contribute to AdGuard in other ways.
[](https://github.com/AdguardTeam/KnowledgeBase/edit/master/docs/general/ad-filtering/adguard-filters.md)
[Previous How ad blocking works](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)[Next Search ads and self-promotion](https://adguard.com/kb/general/ad-filtering/search-ads/)
  * [AdGuard filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/#adguard-filters)
  * [AdGuard Filters Policy](https://adguard.com/kb/general/ad-filtering/adguard-filters/#adguard-filters-policy)
  * [Contributing to AdGuard filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/#contributing-to-adguard-filters)
    * [Report Issues](https://adguard.com/kb/general/ad-filtering/adguard-filters/#report-issues)
    * [Suggest Filtering Rules](https://adguard.com/kb/general/ad-filtering/adguard-filters/#suggest-filtering-rules)
    * [Other ways to contribute](https://adguard.com/kb/general/ad-filtering/adguard-filters/#other-ways-to-contribute)


AdGuard
  * [Official website](https://adguard.com)
  * [About](https://adguard.com/contacts.html)
  * [Blog](https://adguard.com/blog/index.html)
  * [Discuss](https://adguard.com/discuss.html)
  * [Support AdGuard](https://adguard.com/support-adguard.html)


Products
  * [For Windows](https://adguard.com/adguard-windows/overview.html)
  * [For Mac](https://adguard.com/adguard-mac/overview.html)
  * [For Android](https://adguard.com/adguard-android/overview.html)
  * [For Android TV](https://adguard.com/adguard-android-tv/overview.html)
  * [For iOS](https://adguard.com/adguard-ios/overview.html)
  * [For browsers](https://adguard.com/adguard-browser-extension/overview.html)
  * [Version history](https://adguard.com/versions.html)


Support
  * [Support Center](https://adguard.com/support.html)
  * [How to create your own ad filter](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
  * [AdGuard Ad Filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
  * [Removal Instructions](https://adguard.com/removal.html)
  * [Userscripts](https://adguard.com/kb/general/extensions/)
  * [FAQ](https://adguard.com/support/faq.html)
  * [AdGuard status](https://status.adguard.com/)
  * [AdGuard diagnostics](https://adguard.com/test.html)


License
  * [Purchase License](https://adguard.com/license.html)
  * [Recover License](https://adguard.com/kb/general/license/what-is/)
  * [Terms of sale](https://adguard.com/terms-of-sale.html)
  * [Get Free License](https://adguard.com/get-adguard-for-free.html)
  * [Distribution](https://adguard.com/partners.html)


![AdGuard](https://adguard.com/kb/img/logo_dark.svg)
© 2009–2026 Adguard Software Ltd.
