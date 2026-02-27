[Skip to main content](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#docusaurus_skipToContent_fallback)
[![AdGuard](https://adguard.com/kb/img/logo.svg)](https://adguard.com/kb/)[Docs](https://adguard.com/kb/)[Blog](https://adguard.com/blog/index.html)[Official website](https://adguard.com)
[](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
  * [English](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
  * [Русский](https://adguard.com/kb/ru/general/ad-filtering/how-ad-blocking-works/)
  * [Deutsch](https://adguard.com/kb/de/general/ad-filtering/how-ad-blocking-works/)
  * [Čeština](https://adguard.com/kb/cs/general/ad-filtering/how-ad-blocking-works/)
  * [Français](https://adguard.com/kb/fr/general/ad-filtering/how-ad-blocking-works/)
  * [Español](https://adguard.com/kb/es/general/ad-filtering/how-ad-blocking-works/)
  * [Italiano](https://adguard.com/kb/it/general/ad-filtering/how-ad-blocking-works/)
  * [Português (Brasil)](https://adguard.com/kb/pt-BR/general/ad-filtering/how-ad-blocking-works/)
  * [日本語](https://adguard.com/kb/ja/general/ad-filtering/how-ad-blocking-works/)
  * [한국어](https://adguard.com/kb/ko/general/ad-filtering/how-ad-blocking-works/)
  * [中文（中国）](https://adguard.com/kb/zh-CN/general/ad-filtering/how-ad-blocking-works/)
  * [中文（台灣）](https://adguard.com/kb/zh-TW/general/ad-filtering/how-ad-blocking-works/)
  * [Help Us Translate](https://adguard.com/kb/miscellaneous/contribute/translate/program/)


[GitHub](https://github.com/AdguardTeam/KnowledgeBase)
Search`K`
[![AdGuard](https://adguard.com/kb/img/logo.svg)](https://adguard.com/kb/)
  * [Overview](https://adguard.com/kb/)
  * [General](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
    * [Ad filtering](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
      * [How ad blocking works](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
      * [AdGuard filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
      * [Search ads and self-promotion](https://adguard.com/kb/general/ad-filtering/search-ads/)
      * [Tracking filter rules statistics](https://adguard.com/kb/general/ad-filtering/tracking-filter-statistics/)
      * [How to create your own ad filters](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
      * [AdGuard filter policy](https://adguard.com/kb/general/ad-filtering/filter-policy/)
    * [HTTPS filtering](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
    * [Phishing and malware protection](https://adguard.com/kb/general/browsing-security/)
    * [Tracking protection (formerly Stealth Mode)](https://adguard.com/kb/general/stealth-mode/)
    * [AdGuard account](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
    * [Extensions](https://adguard.com/kb/general/extensions/)
    * [License](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
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
  * [Miscellaneous](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)
  * [Guides](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/)


  * [](https://adguard.com/kb/)
  * General
  * Ad filtering
  * How ad blocking works


On this page
# How ad blocking works
AdGuard has many ad-blocking products for different platforms, each with its own unique features. But what unites them all is that they block ads and trackers. This article describes how ad blocking works from the inside.
We don't cover DNS filtering here. It's a different way of blocking ads, with its own advantages and disadvantages. Follow this link to [learn more about DNS filtering](https://adguard-dns.io/kb/general/dns-filtering#how-does-dns-filtering-work).
## General principle[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#general-principle "Direct link to heading")
Filter lists, also called filters, lie at the core of any ad blocker. Filters are literally lists of rules written in a special syntax. Ad blockers can understand this complex syntax. They interpret filtering rules and perform actions on web traffic based on what the rules tell them to do: block specific elements, alter web pages in certain ways, etc.
![How ad blocking works](https://cdn.adtidy.org/public/Adguard/Blog/manifestv3/adblockingworks.png)
## Filter lists[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#filter-lists "Direct link to heading")
To better understand ad blocking, it's important to know the underlying principles of how filters work.
Filtering rules that make up filters are not created automatically. They are developed by filter maintainers, including professionals and volunteers, who use browser developer consoles and other tools (such as the AdGuard's filtering log) to determine which rules will block a particular ad or tracker. This description of the process is very simplistic — some ads are particularly hard to block and require multiple rules, multiple iterations, and the use of complex syntax.
And even when a rule finally gets added to a filter, it doesn't mean that it stays there forever. Ads change, ways to serve the same ads on the same websites change, and the filter rules have to change, too. Sometimes rules become obsolete, a new ad appears, or a new filtering rule is needed to block the same ad. Filters are often maintained by one person, but even for a team of maintainers, it's impossible to constantly monitor the entire web. That's why many ad blockers have tools to help users easily report any filter-related issues they encounter.
![Filter update scheme](https://cdn.adtidy.org/public/Adguard/Blog/manifestv3/filtersupdates.png)
AdGuard users [have access to a special web reporting tool](https://reports.adguard.com/new_issue.html). Thanks to user complaints, filter developers can focus on correcting their filter lists and not on scouring the Internet for new and old unblocked ads.
Filters can do more than just block ads. There are filters that block tracking, social media widgets, and annoyances, such as cookie notices. Different users may choose different combinations of filters to match their personal preferences. There are websites like [filterlists.com](https://filterlists.com/) that are dedicated to filter lists and have huge databases.
We develop and maintain [our own set of filter lists](https://adguard.com/kb/general/ad-filtering/adguard-filters/) that can be used with AdGuard or other ad blockers.
## Types of filtering rules[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#types-of-filtering-rules "Direct link to heading")
There are many types of filtering rules that serve different purposes. Depending on the ad blocker you use, and especially on your OS, some types of rules may not be supported.
### Basic filtering rules[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#basic-filtering-rules "Direct link to heading")
To be displayed on a web page or in an app, the ad has to be loaded from a server first. To do so, the browser or the app needs to send a web request. The most basic way of preventing an ad from appearing on your screen is to block this request so it never reaches the server, and thus there's no reply.
Basically, all AdGuard Ad Blocker products can block web requests according to the active filter rules. This method is very effective at stopping the ad, but it has some drawbacks. The most obvious one is: whatever place an ad was taking up will be left empty or occupied by an ad leftover.
### Cosmetic filtering rules[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#cosmetic-filtering-rules "Direct link to heading")
Every web page has a Document Object Model (DOM), an HTML document containing the structure and elements of this page. As ads are also page elements, they get recorded in the DOM. Ad blockers can remove parts of the DOM, while filtering rules help them understand which parts are ads and should be removed, and which parts should be left intact.
This method allows you to avoid above-mentioned blank spaces and ad leftovers, as well as perform other more complicated tasks.
### HTML filtering rules[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#html-filtering-rules "Direct link to heading")
In most cases, it's enough to use the above-mentioned basic and cosmetic rules to filter ads. But when it is necessary to change the HTML code of the page itself before it is loaded, you need filtering rules for HTML content. These rules allow you to specify the HTML elements to be cut out before the browser even loads the page.
These rules are quite complicated and require the ad blocker to be granted certain access rights, so not all platforms support them. Currently, these rules work only in the AdGuard Firefox add-on and in the AdGuard apps for Windows, Mac, and Android.
There are other types of filtering rules, but they require more advanced technical knowledge to understand how they work. If you are interested, [check out our comprehensive guide on filtering rules in the linked article](https://adguard.com/kb/general/ad-filtering/create-own-filters/).
## Types of request handling in AdGuard[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#types-of-request-handling-in-adguard "Direct link to heading")
AdGuard handles requests according to filters, user rules and settings enabled by the user. As a result, a request can be blocked, modified, allowed or, when nothing is done to it, just processed.
Detailed information on how each request of yours has been handled by AdGuard can be found in the _Filtering log_ (AdGuard for Windows, AdGuard for Mac, AdGuard Browser Extension) or _Recent activity_ (AdGuard for iOS, AdGuard for Android).
Regarding AdGuard filters, you can also check [our filter policy](https://adguard.com/kb/general/ad-filtering/filter-policy/), which describes in detail what and why each of our filters blocks.
### Examples of blocked requests[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-blocked-requests "Direct link to heading")
AdGuard DNS filter blocks requests to ad domains, such as `ad.doubleclick.net`.
AdGuard Tracking Protection filter blocks tracking requests, such as `youtube.com/youtubei/log_event?`.
### Examples of allowed requests[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-allowed-requests "Direct link to heading")
AdGuard Base filter allows non-ad requests, such as `www.google.com/complete/search?q=`.
Filter unblocking search ads and self-promotion allows requests to search ad-related domains, such as `www.google.com/aclk?`.
Requests to websites that are added by the user to _Allowlist_ are allowed.
### Examples of modified requests[​](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-modified-requests "Direct link to heading")
Tracking protection feature with protection level set to _High_ enables AdGuard URL Tracking filter which modifies requests by removing tracking parameters from them:
`https://www.rentio.jp/products/ax-n1b?click_from=top_newitems` → `https://www.rentio.jp/products/ax-n1b`
`https://www.baseballchannel.jp/npb/183688/?ref=ise` → `https://www.baseballchannel.jp/npb/183688/`
`https://www.gog.com/game/spec_ops_the_line?pp=2863d7ae605104eeef364e3f164d3404e20f680c&gad_source=1` → `https://www.gog.com/game/spec_ops_the_line`
Please note that _modified_ events you see in the Filtering log or Recent activity refer not only to the cases when a request is modified, but also when:
  * something on the page is changed (usually by cosmetic rules)
  * the response is modified


[](https://github.com/AdguardTeam/KnowledgeBase/edit/master/docs/general/ad-filtering/how-ad-blocking-works.md)
[Previous Overview](https://adguard.com/kb/)[Next AdGuard filters](https://adguard.com/kb/general/ad-filtering/adguard-filters/)
  * [General principle](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#general-principle)
  * [Filter lists](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#filter-lists)
  * [Types of filtering rules](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#types-of-filtering-rules)
    * [Basic filtering rules](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#basic-filtering-rules)
    * [Cosmetic filtering rules](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#cosmetic-filtering-rules)
    * [HTML filtering rules](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#html-filtering-rules)
  * [Types of request handling in AdGuard](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#types-of-request-handling-in-adguard)
    * [Examples of blocked requests](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-blocked-requests)
    * [Examples of allowed requests](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-allowed-requests)
    * [Examples of modified requests](https://adguard.com/kb/general/ad-filtering/how-ad-blocking-works/#examples-of-modified-requests)


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
