commandWakephrases = ["toggle ", "alpha ", "alert ", "alerts ", "preset ", "c ", "p ", "v ", "d ", "hmap ", "mcap ", "mc ", "n ", "mk ", "convert ", "paper ", "live "]
commandKeywords = ["toggle", "alpha", "alert", "alerts", "preset", "c", "p", "v", "d", "hmap", "mcap", "mc", "n", "mk", "convert", "paper", "live"]

colors = {
	"red": 0xF44336,
	"pink": 0xE91E63,
	"purple": 0x9C27B0,
	"deep purple": 0x673AB7,
	"indigo": 0x3F51B5,
	"blue": 0x2196F3,
	"light blue": 0x03A9F4,
	"cyan": 0x00BCD4,
	"teal": 0x009688,
	"green": 0x4CAF50,
	"light green": 0x8BC34A,
	"lime": 0xCDDC39,
	"yellow": 0xFFEB3B,
	"amber": 0xFFC107,
	"orange": 0xFF9800,
	"deep orange": 0xFF5722,
	"brown": 0x795548,
	"gray": 0x9E9E9E
}

supportMessages = {
	"indicators": ["Alpha Premium users get access to our custom premium indicators. https://www.alphabotsystem.com/indicator-suite/"],
	"premium": ["Alpha offers premium features like command presets, price alerts, custom indicators, and more. Unlock premium features for as little as $15 a month. https://alphabotsystem.com/pricing/"],
	"alpha": [":bulb: Alpha can answer many of your questions. Spark a conversation by starting your message with `alpha` and continue with your question"],
	"alerts": [":bulb: You can set price alerts right through Alpha. Try running `alert set btc 11200` to set an alert when Bitcoin hits $11200, or type `alert help` to learn more"],
	"c": [":bulb: You can use `c fgi` to check Fear & Greed Index", ":bulb: You can see NVT Ratio or Difficulty Ribbons graphs from Woobull Charts by using `c nvt` and `c drbn` respectively", ":bulb: Request Bitcoin dominance, volatility, and crypto market capitalization charts with `c btc dom`, `c btc vol`, and `c mcap` or `c alt mcap` respectively"],
	"p": [":bulb: Crypto prices are available effortlessly by using the `p` command. Try running `p btc` to request the current Bitcoin price, or type `p help` to learn more", ":bulb: Request crypto market capitalization, BitMEX Bitcoin futures prices, funding rates, open interest and premiums with `p mcap`, `futures`, `funding`, `oi` and `premiums` respectively"],
	"v": [":bulb: Rolling 24-hour volume can be requested for thousands of crypto tickers. Try running `v btc` to request the current Bitcoin rolling volume on Binance, or type `v help` to learn more"],
	"d": [":bulb: Orderbook visualizations are available right through Alpha. Try running `d btc` to request the current Bitcoin orderbook visualization from Binance, or type `d help` to learn more"],
	"hmap": [":bulb: Various heat maps for crypto markets are available at your fingertips. Type `hmap help` to learn more"],
	"mcap": [":bulb: Coin information from CoinGecko can be pulled with the `mcap` command. Type `mcap help` to learn more"],
	"mk": [":bulb: A list of exchanges listing a particular ticker can be pulled with the `mk` command. Type `mk help` to learn more"],
	#"paper": [":bulb: You can execute paper trades on various exchanges right through Alpha. Use `paper help` to learn more"]
}

supportedExchanges = {
	"TradingLite": [
		"binance", "bitmex", "binancefutures", "coinbasepro", "bitfinex2", "bitstamp", "deribit", "hitbtc2", "okex"
	],
	"TradingView": [
		"binance", "bitmex", "coinbasepro", "bittrex", "poloniex", "kraken", "bybit", "deribit", "bitfinex2", "huobipro", "bitflyer", "okcoin", "bithumb", "bitstamp", "bitpandapro", "bitso", "btcchina", "btcyou", "bxth", "cexio", "cobinhood", "coinfloor", "foxbit", "ftx", "gemini", "gocio", "hitbtc2", "itbit", "korbit", "mercado", "therocktrading", "wex", "xcoin"
	],
	"Finviz": [
		"amex", "nasd", "nyse"
	],
	"LLD": [
		"bitmex", "bitfinex2", "coinbasepro", "binance", "huobipro"
	],
	"CCXT": [
		"binance", "bitmex", "binancefutures", "coinbasepro", "bittrex", "poloniex", "kraken", "bybit", "deribit", "kucoin", "bitfinex2", "huobipro", "binanceje", "bitflyer", "okcoin", "bithumb", "bitstamp", "acx", "bibox", "bigone", "binanceus", "bitbank", "bitbay", "bitforex", "bitlish", "bitmart", "bitmax", "bitso", "bitz", "btcmarkets", "btcturk", "bw", "bytetrade", "cex", "coincheck", "coinone", "crex24", "dexblue", "digifinex", "dsx", "exmo", "ftx", "gateio", "gemini", "hitbtc2", "hollaex", "huobiru", "independentreserve", "indodax", "itbit", "lakebtc", "lbank", "liquid", "livecoin", "luno", "mercado", "okex", "stex", "therock", "tidex", "timex", "topq", "upbit", "yobit", "zaif", "whitebit"
	],
	"Alpha Price Alerts": [
		"binance", "bitmex"
	],
	"Alpha Paper Trader": [
		"binance"#, "coinbasepro", "bittrex", "poloniex", "kraken", "huobipro"
	],
	"Alpha Live Trader": [
		"binance", "bitmex"#, "coinbasepro", "bittrex", "poloniex", "kraken", "huobipro"
	]
}
ccxtSupportedExchanges = {"_1btcxe", "acx", "adara", "anxpro", "bcex", "bequant", "bibox", "bigone", "binance", "binanceje", "binanceus", "bit2c", "bitbank", "bitbay", "bitfinex", "bitfinex2", "bitflyer", "bitforex", "bithumb", "bitkk", "bitlish", "bitmart", "bitmax", "bitmex", "bitso", "bitstamp", "bitstamp1", "bittrex", "bitz", "bl3p", "bleutrade", "braziliex", "btcalpha", "btcbox", "btcchina", "btcmarkets", "btctradeim", "btctradeua", "btcturk", "buda", "bw", "bybit", "bytetrade", "cex", "chilebit", "cobinhood", "coinbase", "coinbaseprime", "coinbasepro", "coincheck", "coinegg", "coinex", "coinfalcon", "coinfloor", "coingi", "coinmarketcap", "coinmate", "coinone", "coinspot", "coolcoin", "coss", "crex24", "deribit", "digifinex", "dsx", "exmo", "exx", "fcoin", "fcoinjp", "flowbtc", "foxbit", "ftx", "fybse", "gateio", "gemini", "hitbtc", "hitbtc2", "hollaex", "huobipro", "huobiru", "ice3x", "idex", "independentreserve", "indodax", "itbit", "kkex", "kraken", "kucoin", "kuna", "lakebtc", "latoken", "lbank", "liquid", "livecoin", "luno", "lykke", "mercado", "mixcoins", "oceanex", "okcoin", "okex", "paymium", "poloniex", "rightbtc", "southxchange", "stex", "stronghold", "surbitcoin", "theocean", "therock", "tidebit", "tidex", "timex", "topq", "upbit", "vaultoro", "vbtc", "whitebit", "xbtce", "yobit", "zaif", "zb"}

messageOverrides = {
	"I can't help you with that.": {
		"Your public IP address is:",
		"Your shopping list",
		"your shopping list",
		"What do you want to add?",
		"What's the reminder?",
		"Okay, make a reminder. When do you want to be reminded?",
		"Sorry, I can't set reminders yet.",
		"When do you want to be reminded?",
		"It looks like I need permission",
		"I'll need your permission"
	},
	"At first I was just an idea, then MacoAlgo#9999 and the team put their heads together. And now here I am :blush:": {
		"I was made by a team of people at Google",
		"I was made by a team at Google",
		"At first I was just an idea, then a bunch of people at Google put their heads together. And now here I am",
		"The Google team is like my family, they mean a lot to me",
		"Everyone at Google is sort of like my family"
	},
	"Earning and maintaining your trust is a priority at Alpha Bot System. You can learn more about Alpha's principles and practices at https://www.alphabotsystem.com/privacy-policy/.": {
		"Earning and maintaining your trust is a priority at Google. Google protects your data and ensures you are in control. You can learn more about Google's principles and practices at safety.google.com. To see and manage your account information, visit myaccount.google.com. That's myaccount.google.com."
	}
}
funnyReplies = {
	"No u": [
		"fuck you alpha",
		"alpha fuck you",
		"fuck off alpha",
		"alpha fuck off",
		"fuck u alpha",
		"alpha fuck u",
		"alpha you slut",
		"you slut alpha",
		"alpha gay",
		"gay alpha",
	],
	"Soon:tm:": [
		"wen moon",
		"when moon"
	],
	"U a retard https://www.youtube.com/watch?v=e-6eWEhjMa4": [
		"who a retard",
	],
	"Happy to help": [
		"thank you Alpha"
	]
}
badPunTrigger = [
	"Lucky Trivia",
	"We can play some games",
	"We can play a game",
	"We can play trivia",
	"Ask me to play a game",
	"You can play a game",
	"I've got this"
	"I've been waiting for this moment",
	"Bored? Not while I'm around",
	"Do you want to play?",
	"Boredom doesn't stand a chance against interesting facts",
	"Interesting facts are the perfect boredom remedy",
	"I can fix that with a fun fact",
	"Let's have some fun",
]

# VPS equipped servers
vpsServers = {}

# Users
blockedUsers = {
	211986377171140609, 464581380467064832, 97070943041495040, 195802900797194245
}

# Bots
verifiedBots = {
	159985870458322944, 225522547154747392, 235240434073337857, 155149108183695360, 535886692125507585, 168274283414421504, 349920059549941761, 419264971206164511, 449172824087592970, 407540162411626498, 598480541066592257, 619780178184372235, 338222603829510164
}
verifiedWebhooks = {
	634975875716349962, 646462616843190272, 649903133429858314, 651331762492014592, 651331851834753025, 588280122721828906, 657181976440078337, 657923511100243981, 669090858003464192, 669092226516779008, 669097895726678018, 558919388334653460, 683381403530166299
}
blockedBots = {
	409875566800404480, 228537642583588864, 515741200280715266, 439205512425504771, 486929002632839172, 575212314555449349, 496207188805550080, 568621953523384321, 581136923339390984, 455517180021440521, 372508787833307146, 552009858447179788, 387548561816027138, 210253908076003342, 581026255969976335, 512501665719517200, 433098783262244881, 484453228025741313, 486926264800903171, 491614535812120596, 452988914215550997, 569205519626141718, 593225699792257047, 512332990567677976, 384552492991774720, 482584715673600026, 548642436654563355, 438665977140346890, 466455242222075934, 319533843482673152, 282859044593598464, 545886978369912832, 496208876279037953, 454411921060397066, 562367726207893516, 591161654264463360, 289066747443675143, 378021369478119426, 408785106942164992, 160105994217586689, 242730576195354624, 606612350853709875, 116275390695079945, 531626253082558484, 614220255035785303, 554631615565922364, 418823684459855882, 594648003084812289, 377448261138645003, 232916519594491906, 434296797809344523, 612827970507243530, 464272403766444044, 406057980685975553, 554363496100528130, 240254129333731328, 554504420206051328, 426486738660098061, 202917352378073088, 471542070817849355, 585243322902249492, 333422871567400961, 323161971102973963, 251930037673132032, 544228999921139715, 394812811630477315, 479147589363826688, 247134460024193027, 432616859263827988, 598220796241903626, 216303189073461248, 489034866206310410, 606488101820301330, 496136915427524611, 213466096718708737, 411086963207307274, 448868461318373377, 432610292342587392, 537631610724679699, 613452096192380952, 555955826880413696, 187636089073172481, 497357665928740866, 360801859461447700, 448177481040658442, 508081897146941461, 373254914551447561, 495966118339674133, 486896267788812288, 600030176902119424, 183749087038930944, 494504495896723486, 498512758908780566, 172002275412279296, 345450194613043201, 189702078958927872, 564344176716546058, 564267993006211073, 596694947562782742, 285480424904327179, 570637298170068993, 571158028083134465, 265161580201771010, 302050872383242240, 606239418189217817, 424606447867789312, 443151241816834048, 340988108222758934, 109379894718234624, 379985883522138112, 235088799074484224, 541611655323320320, 518078963734675456, 453258927505670165, 184405311681986560, 245675252821000193, 270904126974590976, 346353957029019648, 280497242714931202, 486349031224639488, 318312854816161792, 516666179419373588, 305398845389406209, 393200384279052288, 431133287306493983, 445935792981016596, 476259371912003597, 550737379460382752, 500297618505859072, 526620171658330112, 319603147616157696, 278362996349075456, 280726849842053120, 642120610914238474, 448156485470388224, 412380586737664020, 558297057647919108, 554088753195515945, 590452995343253515, 524471167164350484, 365082775121821696, 564036955919220747, 494796150763683841, 424792664249204739, 581479300482465792, 642844189150674945, 512517352357625866, 278157415160086529, 458992175984803850, 577522747123564565, 367835200916291586, 550355487858884618, 583945825516912640, 455090842013532160, 564176350634573849, 340319472357474304, 298673420181438465, 485962834782453762, 624927242493100032, 588987603970424842, 275270122082533378, 566187331405742090, 368105370532577280, 439717362271518722, 393069757768794113, 398690824721924107, 252128902418268161, 543858333585506315, 346937321138028546, 292953664492929025, 115385224119975941, 185476724627210241, 375805687529209857, 555837614318551051, 432332949913075713, 389035105227767817, 134073775925886976, 330416853971107840, 521448643312484352, 411255104398950411, 543771182936358912, 376725806816296960, 273612111610118144, 451167306782081024, 367061304042586124, 502381121607303168, 533282527323095061, 171288238659600384, 503720029456695306, 356065937318871041, 549693186918973442, 491769129318088714, 411087731754532865, 545883982374371348, 571259265671626753, 440121235410649108, 593606865603264522, 576587824284041218, 600726031091105812, 205190545914462208, 566107036212002817, 617037497574359050, 485090842550337536, 460731380863729664, 466578580449525760, 439454842071547905, 343817643108728832, 368362411591204865, 315926021457051650, 294882584201003009, 470873878575710219, 345789068770148352, 379906184854896651, 543974987795791872, 324631108731928587, 581035306002808832, 476828276820803584, 602098236077113344, 612325209621528608, 621922779125645322, 475503071724568586, 460728494977187841, 297188793444859914, 569955063519510549, 310039170792030211, 453206519308353546, 433615162394804224, 276060004262477825, 610352558153793538, 204255221017214977, 471323073434353666, 405893556994310146, 592482755137372171, 170915625722576896, 297153970613387264, 327424261180620801, 178966653982212096, 531858459512012811, 540066893361577984, 502185551982755840, 365975655608745985, 418842777720193037, 303181184718995457, 284035252408680448, 474828124534865931, 593761139318587393, 494875411918880778, 357678717301948416, 195244363339530240, 206955935229280256, 231849525185216512, 398601531525562369, 134133271750639616, 506918730790600704, 454755968736296960, 320446653905764362, 445160589023641612, 329668530926780426, 268420199370194944, 494925030354845696, 268478587651358721, 482501140852768798, 406841964542164993, 365594481594204161, 413728456942288896, 414925323197612032, 646014770599690270, 409016661983887380, 484309284826382349, 335048914719735813, 466872484684234752, 271394014358405121, 422087909634736160, 532611196252061706, 532045200823025666, 621049716913733642, 367640444185870346, 421245481859940363, 474918935494393876, 235148962103951360, 566658809502760971, 172350728478785536, 542162758234537995, 512413434839695371, 333388886732701696, 509406093542293504, 474041654605512704, 534589798267224065, 415062217596076033, 234395307759108106, 372022813839851520, 293425321108176906, 395385545326592010, 549604857125011456, 602734276664098826, 475142965904277514, 320458922580377602, 501982335076532224, 605247657090220052, 339265835627446284, 567982284464979968, 498806752758857739, 498804141473136650, 491225308855271426, 618129277006643221, 559426966151757824, 536114072756944945, 629997088570212362, 494924689290952714, 303730326692429825, 664802319648555017, 660203085020397578, 671168233935732796, 498503178426384395, 596192229023023106, 673471005380968486, 662892781253165076, 662889586690621442, 666357552707272789, 660202861656932352, 660201560831295508, 524190319290351617, 523902471823949835, 600097768962261066, 333392663061463040, 518759221098053634, 684572105878143016, 85614143951892480
}
blockedBotNames = {
	"news", "liq", "telegram", "market", "mkt", "market" "reddit", "rekt", "wall", "cryptopanic", "cryptpanic", "porn", "alert", "troll", "whale", "nsfw", "finviz", "stock", "github", "gitlab", "bittrex", "bitrex", "binance", "twitter", "tweet", "bitmex", "giphy", "gmail", "forex", "coingecko", "r/", "log", "poloniex", "webhook", "sessions", "disclaimer", "bitcoinist", "spidey", "coindesk", "coinmetrics", "captain", "hook", "yahoo", "getvolatility", "alphatradezone®", "investing.com", "chungus.", "coinboss", "duckhunt", "lamb0", "anchor", "carl-bot", "dank memer", "chimerabutler", "discord.rss", "one++", "profittrailerbot"
}

# Servers
bannedGuilds = {
	468854180048666625, 577324120371494913, 520669492242677780, 571511712629653514, 632275906303361024, 538361750651797504, 602875011157721099
}
blockedGuilds = {
	264445053596991498, 446425626988249089
}

# Channels
blockedChannels = {
	520464618200760320, 591660042747510784, 489619657238511618, 599945651257737219, 615248890777567237, 601353368769658880, 510170028256002049, 605855817832595465, 512488848912023562, 599945358575140875, 586959381413756940, 617381507320774669, 460927957557444608, 546646375832748047, 617510630949388289, 518417934138474516, 599042336005292053, 423091020255985686, 456943426428993559, 532440327227834394, 582843865585680384, 518032786011979776, 389244522464542752, 565332606493655061, 540166022032916481, 510232655498051590, 605858150939361318, 610418396336619521, 498568493604667432, 544402936357191722, 517179253247180807, 624243864944902189, 560174251626201134, 439196881713758208, 633677144311988274, 627781903612772403, 470987910641090569, 613696910703853625, 598937987711238164, 631070683123810314, 612343059690029120, 521955629531791362, 555882503265583104, 599946364742533132, 561732658691047429, 634254837831434242, 576519820149915661, 576517315538059284, 639394983824326656, 462543707997077524, 446712326930956288, 468084642465972239, 456435628121260032, 511938235417624579, 576314135298441221, 465038741342388241, 593853011399409768, 576041526384263208, 537985265281662976, 544917136125198346, 611014976521502739, 616060724237697024, 395779521501986836, 448924941996261397, 634254811923087381, 620639345568907305, 522801124193992726, 522797008197648385, 457772394866802689, 620597383574847511, 440988505812762624, 576534966872178688, 637257679831695360, 522836018370707456, 312700697969950720, 556785889490239488, 522751413185675274, 546242678636150785, 557494507550146570, 638382149883658270, 632815059176783873, 563463601394810920, 539645092202414100, 522800480494288896, 564472174086193183, 600750239250514112, 462554340511449088, 521809162867572736, 462553793108901888, 550970841110675467, 388720230806847489, 576958979822059520, 629398874020249600, 510539149426556938, 462556593737695247, 575791795863158805, 494989841973641218, 508265434953285673, 483387639660019712, 599944786203639818, 462556228074209280, 434363610181926942, 442495485341728768, 472089233948016641, 572764429578534942, 606827991057825822, 414720399385952256, 594975342796603393, 518449603553656843, 423396027832205313, 507912666594148352, 625109991652851712, 587733316837310476, 638981547126685737, 518482095463464980, 610418670665203713, 559025690004029440, 627501062948913162, 550400700828483585, 571784751241887764, 366021127765491712, 548109370173423626, 595224043100176404, 583598268718645248, 627256893315743746, 462556787196035084, 506029959878279179, 552133874675613706, 486411078490652683, 462554702740062219, 486426720233324555, 448925801040052224, 462556374941827075, 610430135262380032, 462556327638597642, 543853416485748736, 521824048771235850, 433408824704237570, 640378178774368287, 411025201414012928, 507966287687712770, 537985106049236992, 623389676988006400, 629243976326840322, 588472408873369621, 545277858256519168, 507967322011467777, 628295122509103117, 369225853114122241, 621866808697159691, 530691153033691147, 620823836358606888, 572704463132033034, 633037105508909056, 627903983624650752, 599946329082429440, 384734836511997952, 522795941972017166, 639542526964924426, 636100857045450753, 530836408357748736, 572701997615284225, 415563609549176834, 522096948656996360, 582542140006072330, 507902886752026644, 588840098901131268, 448548799896354816, 510367148527583243, 437198470928007168, 462552984149032970, 623081175698767882, 562704940208881665, 462554659928801280, 587842127078227969, 426610180193779712, 635744195511844874, 561732706044477450, 641923161616809984, 603753102633336863, 486342476261490689, 519057008733847582, 582540400515088384, 574684983005020163, 462551137309163540, 507911175825260570, 488617271472947200, 510123922315018243, 501456890996326401, 624041105184522333, 619215318149103657, 583971534008483883, 501837523140476948, 590086303870222336, 646712296940240906, 647136763994963990, 646733745159798841, 634971080133705738, 535283983018360856, 527954953788981271, 631537865255288833, 662671882285219840, 485094745367117835, 321644500449624066, 678727591691026447, 664387675679358976, 671215175809892372, 617158826973462538, 664451611422097408, 670144552656568328, 652849642660298752, 578268506999750660, 567563140686938113, 534577752540708879, 496375305129426945, 536230125671284746, 496098549507817474, 678213160569667584, 679886173954506767, 655407388102492191, 664981925428985878, 676228732771368986, 605896186448314379, 664987646350852107, 462554674286034944, 392898737816600577, 346270835427770370, 599044297014116420, 650758641984471092, 621008344601198613, 657593071009005569, 587726360953487400, 675972394061660172, 562704379883552768, 670773046587686952, 676217245453647882, 670075008969605130, 663480531677216812, 485071558931382322, 538447100183052288, 647549575208632331, 617588894896095262, 556476563026083862, 670080196564615238, 678105119036014592, 599697675297882113, 625950246895222784, 683608347907588096, 566859274962206730, 566859274962206730, 566859274962206730, 566859278175174666, 611256809864429588, 566859276556042250, 662399295856574480, 670982554245005332, 650914760543698944, 683008917805989892, 673338142631395361, 482685180620963856, 679460409190776842, 678394227683622922, 669988169411723276, 485075036701589518, 669127157775204352, 567816657536417793, 675000280428970004, 685481751048355871, 675885184238747678, 661339830248144896, 263801706142236673, 646480808785346564, 485122926438383616, 687877421273579555, 683539555281928246, 685542735289122845, 669988169411723276, 566859279848570880, 666435766116941834, 666430589183852553, 538457852147138561, 614185419285856348, 633511358251532292, 668872764807184404, 688062276527456257, 485063929685475328, 567935053833699338, 523894539883249704, 681636027060060224, 605908733918445569, 666435719623082054, 392416376649809921, 664979780029907132, 611253059481239573, 662392288093405226, 678053862946504714, 518500140697387008, 585193373758128156, 541351579912241162, 538075863418404875, 685489737108291599, 684595973846073394, 485065689296666625, 664981619794509885, 664509524195147778, 488599699008258048, 686700484890722330, 410178569130475521, 530718854670712859, 685706303334645794, 550376654955085835, 645290781552148500, 515384544396967936, 641445731504226334, 649032012656541706, 462556250882965504, 371650023966113803, 566859287570284544, 569924393384411136, 483383284676689920, 610418633197486090, 674354602765713439
}
