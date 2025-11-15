# Question

Part C: Critical Analysis 

Component 2: Original Variable Design (5 points, ~150-200 words)

Propose a NEW binary variable (one not in the dataset) to test against Meridian's equity returns:
What is your proposed binary variable and why would it provide meaningful strategic insights?
Which group do you expect to have higher equity returns and why?
If you found statistically and practically significant results, what would this tell management about their equity strategy?


# Rubric:
But here are common reasons why points were deducted: 
 - Part C, Component 2
Not proposing a binary variable that was monthly (or not explicitly mentioning that)
Proposing a binary variable from the dataset (needed to be a NEW variable)
Proposing a binary variable related to individual stocks, rather than measures that might affect an entire portfolio
Lack of specificity with recommendations to management

Exceptional Answers to Part C of Open-Ended
Questions
Part C: Part 3
Student Answer 1:
I am proposing the binary variable of “US dollar strength.” In practice, this variable would be
categorized as either “Strong” or “Weak” in relation to the currencies of other countries. The basis
for this categorization would be the USDX, with a time with a USDX > 100 corresponding to “Strong”
and a time with a USDX < 100 representing “Weak.” Based on my understanding of
macroeconomics, I would expect times with a “strong” USD rating to have lower equity returns
than a “weak” USD rating, as foreign citizens and investors would have less comparative liquidity to
invest in US equities. We recently saw the impact of FOREX on equity markets in the first part of
President Trump’s term, as the dollar lost a substantial amount of value. Meridian could shift to
equities with a strong emphasis on imports, as a “Strong” USD would allow greater import power to
those companies. If there were statistically significant results, Meridian would have to shift away
from equity exporters and change the makeup of its equities. The strategic makeup of Meridian’s
investments would need to shift within each category (bond & equity) if there were a significant
difference between times of “Strong” and “Weak.”
Student Answer 2:
My proposed binary variable would be “flow_stress_lag1”.
This variable would flag all months after heavy investor withdrawals. I’d set it to 1 for month t when
client flows in month t-1 were in the bottom quartile of the sample (like client_flows_{t-1} ≤ Q1), 0
otherwise. The reasoning in one month behind is to avoid simultaneity between flows and returns
and make the indicator ex-ante for returns in month t. This then is strategically useful as a proxy for
liquidity pressures that force the equity book to trim positions, trade at worse prices, or miss
entries altogether. Consequently, my variable aims at exact pressures and investor behavior that
link to execution capacity or alpha capture. This reveals elements chipping away at Meridian
Capital’s steady and risk-adjusted perception.
For direction, I expect lower equity returns in months with flow_stress_lag1 = 1 and higher returns
when it equals 0, because redemptions typically lead to de-risking, trading frictions, and reduced
optionality. If tests yielded a statistically/practically significant difference, it would indicate that
flow dynamics do in fact predict next-month equity performance. If so, I’d tell management to (1)
raise target cash buffers during outflow periods, (2) pre-fund temporary liquidity or hedges around
redemption windows, and (3) tighten exposure caps and position sizing after large outflows to their
current equity strategy. No statistically/practically significant difference would suggest current
liquidity management already protects equity performance.
Student Answer 3:
My proposed binary variable examines the Global Economic Policy Uncertainty Index and
separates it into high uncertainty vs low uncertainty. I define a high uncertainty environment as any
2
point where the index reaches above its 75th percentile of its values since the beginning of the
fund’s data collection (Jan 1, 2019). Anything below this 75th percentile threshold is considered a
low uncertainty environment. This metric would provide meaningful insights because the key
drivers of inflation are derived from both monetary and fiscal policy uncertainty around the globe,
which this index seeks to directly measure. Seeing as the firm’s strategy centers around skillfully
navigating macro factors, I would expect their performance to be better during periods of high
uncertainty, as their active strategy would allow them to capture more value in these situations. If I
found statistically and practically significant results showing otherwise, it would indicate that the
firm’s inflationary and active repositioning strategies don’t work and their fee structure is not
justified, As meridian fails to add value to clients portfolios during the high-stress, inflationary
environments that clients pay them to navigate.
Citation: Davis, Steven J., 2016. “An Index of Global Economic Policy Uncertainty,”
Macroeconomic Review, October.
Student Answer 4:
Proposed Binary Variable: Presidential election-year periods. This variable captures a regime
characterized by heightened political uncertainty, policy risk, and investor sentiment shifts as
elections approach, occur, and resolve. Strategically, it is relevant for Meridian because the firm’s
equity strategy emphasizes tactical responsiveness and macro-oriented positioning. Testing
whether equity returns differ significantly between election-year months and non-election-year
months provides insight into how effectively the fund’s active equity management performs under
political and policy-driven stress. I expect non-election-year months to show higher average equity
returns, since Meridian tends to perform better during stable, low-volatility conditions. Election
years often coincide with volatility spikes, and because Meridian typically adopts a bond-heavy
stance during such periods, weaker equity returns may reflect intentional risk reduction rather than
underperformance. If the t-test revealed significantly lower equity returns during election years, it
would signal that the firm’s defensive approach limits equity upside but enhances stability.
Conversely, if returns are significantly higher in election-year months, it would suggest that
Meridian’s usual bond-heavy positioning during volatile periods may be overly cautious, and that
adopting


# Student Answer:
My new proposed binary variable would be the elected president's political party, which provides insight into whether our strategies need adjustment based on the political orientation of the United States. For the simplest purposes, I would divide it between Democratic and Republican. I’m not quite sure which one I would expect to be better. Republicans market a stronger emphasis on nurturing businesses and potentially benefiting the markets, but empirically, I’m skeptical that this is entirely true. President Trump recently signed into law the Tax Cuts and Jobs Act, which created massive corporate tax cuts aimed at supporting business. It’s possible this would lead to higher credit ratings and other such factors, increasing bond prices. Or, in a slightly different vein, equity returns might increase slightly but be accompanied by a substantial increase in risk when a problematic political party enters office.  If this were to happen, and the American future is more uncertain, I might shift away from the now riskier equity strategy and allocate more of the fund to stable bond offerings. If I found statistically significant results with this, management might need to tweak their strategy when new presidents get elected to better maximize risk-adjusted returns.