Zacharia Kline
May 2, 2022
Documentation on the bayesian filter that differentiates between
Elon Musk tweets and Donald Trump tweets.

Dataset Sizes:
Number of Elons tweets: ~34000
Number of Trumps tweets: ~56000
During the process of collecting this data from their csv files I remove
any emojis and URLs since that is useless data. Im choosing to leave in the 
mentions and hashtags since Elon could @Tesla and #space while Trump could @GOP and #America which would
help the decision process. For Trump tweets specifically I removed retweets.
-----------------
A note about test tweets from Trump: Since his account is suspended I cannot find 'new' tweets so in the training
data, I am skipping the first 10 lines and will use those to test.

A note about test tweets from Musk: I will use his more recent tweets for testing (post March 2022) since 
the dataset includes his tweets starting from 2010 to March of 2022. 

vvvvv After runing the bayesianfilter.py file, try these tweets vvvvv
-----------------
classify('Republicans and Democrats have both created our economic problems.') - Trump
classify('I was thrilled to be back in the Great city of Charlotte, North Carolina with thousands of hardworking 
American Patriots who love our Country, cherish our values, respect our laws, and always put AMERICA FIRST!') - Trump
classify('The Unsolicited Mail In Ballot Scam is a major threat to our Democracy!!!') - Trump
classify('Getting a little exercise this morning!') - Trump

classify('Watch Falcon 9 launch 53 Starlink satellites to orbit') - Musk
classify('Video of Dragon’s Draco thrusters moving the spacecraft closer to the @Space_Station') - Musk
classify('Next I’m buying Coca-Cola to put the cocaine back in') - Musk
classify('Raptor 2 rocket engines at Starbase, each producing over half a million pounds (230 tons) of force') - Musk