import matplotlib.pyplot as plt
import pandas as pd

# read_csv CSV into DataFrame
ip_to_isp = {
    "2a0d:3344:18fa:4916:f109:b90c:1660:710d": "2a0d:3344:18fa:4916/64",
    "fdcc:1705:6306:16:2c3c:8cd9:35be:5cd6": "fdcc:1705:6306:16/64",
    "fd4e:c6e4:ca93:2:265c:26df:3038:c2a4": "fd4e:c6e4:ca93:2/64"
}

ipv6 = {
    "2a0d:3344:18fa:4916:f109:b90c:1660:710d",
    "fdcc:1705:6306:16:2c3c:8cd9:35be:5cd6",
    "fd4e:c6e4:ca93:2:265c:26df:3038:c2a4"
}

#Prep files here, filter my ips and make sure the sources are shown in a slightly more compact way 
df1_dig = pd.read_csv("csv/dig_querries.csv")
df1_dig = df1_dig[df1_dig["Source"].isin(ipv6)]
df1_dig["Source"] = df1_dig["Source"].replace(ip_to_isp)

df2_dig = pd.read_csv("csv/dig_part2.csv")
df2_dig = df2_dig[df2_dig["Source"].isin(ipv6)]
df2_dig["Source"] = df2_dig["Source"].replace(ip_to_isp)

df3_udp_starlink = pd.read_csv("csv/multiple_websites_tested.csv")
df3_udp_starlink = df3_udp_starlink[df3_udp_starlink["Source"].isin(ipv6)]
df3_udp_starlink["Source"] = df3_udp_starlink["Source"].replace(ip_to_isp)

df4_delete = pd.read_csv("csv/main_addr_delete.csv")
df4_delete = df4_delete[df4_delete["Source"].isin(ipv6)]
df4_delete["Source"] = df4_delete["Source"].replace(ip_to_isp)

df5_delete_back = pd.read_csv("csv/deleted_address_comes_back.csv")
df5_delete_back = df5_delete_back[df5_delete_back["Source"].isin(ipv6)]
df5_delete_back["Source"] = df5_delete_back["Source"].replace(ip_to_isp)

df6_both_used = pd.read_csv("csv/Both_starlink_used.csv")
df6_both_used = df6_both_used[df6_both_used["Source"].isin(ipv6)]
df6_both_used["Source"] = df6_both_used["Source"].replace(ip_to_isp)

#dns concat
df2_dig["No."] += df1_dig["No."].max()

time_diff = df1_dig["Time"].max() - df2_dig["Time"].min()
df2_dig["Time"] += time_diff

dfa = pd.concat([df1_dig, df2_dig], ignore_index=True)
dfa = dfa[dfa["Protocol"] == "DNS"]

# Extract the query type (the part after "query 0x.... ")
dfa["QueryType"] = dfa["Info"].str.extract(r"query\s0x[0-9a-f]+\s+([A-Z]+)")

# Count query types
counts = dfa["QueryType"].value_counts()



#Weird thing concat as well
df5_delete_back["No."] += df4_delete["No."].max()

time_diff_2 = df4_delete["Time"].max() - df5_delete_back["Time"].min()
df5_delete_back["Time"] += time_diff_2

dfb = pd.concat([df4_delete, df5_delete_back], ignore_index=True)

#Truncate repetitve info to shrink the graphs 
df6_both_used = df6_both_used[df6_both_used["Time"] < 1.25]

#df = df[df["No."] < 5000]
#df = df[df["Protocol"] == "DNS"]

# Plots
# nbr of queries and types 
plt.figure(figsize=(8, 5))
total = counts.sum()
ax = counts.plot(kind="bar", figsize=(8,5), label=f"Total queries: {total}")
plt.xlabel("Query Type")
plt.ylabel("Number of Queries")
plt.title("DNS Query Types")
plt.legend(loc="upper right")  
plt.tight_layout()
plt.show()

# IP used for the dns queries 
plt.figure(figsize=(20, 6))  
sources = dfa["Source"].value_counts()
total = sources.sum()
plt.title("Source IP used for DNS queries")
plot = sources.plot(kind="bar", figsize=(8,5), label=f"Total queries: {total}")
plt.ylabel("Number of Queries")
plt.xticks(rotation=0, ha="right")  # rotate 45° and align right
plt.xlabel("Source IP")
plt.legend(loc="upper right")  
plt.show()

# UP/DOWN one ip address to simulate an error / link going down 
plt.figure(figsize=(20, 6))  
plt.title("Source IP used when an error occurs")
plt.plot(dfb["Time"], dfb["Source"], marker=".", linestyle="none")
plt.xlabel("Time [s]")
plt.ylabel("Source IP")
plt.show()

colors = ['#1f77b4', '#ff7f0e']
plt.figure(figsize=(10, 6))  
plt.title("Source IP used when an error occurs")
counts = dfb["Source"].value_counts()
total = counts.sum()
percentages = counts / total * 100
percentages.plot(kind="pie", colors=colors, autopct="%.1f%%")
plt.ylabel("")  # remove y-label
plt.show()

# Normal use with both 
'''plt.figure(figsize=(20, 6))  
plt.title("Source IP used for normal traffic, UCP / TCP ")
plt.plot(df6_both_used["Time"], df6_both_used["Source"], marker=".", linestyle="none")
plt.xlabel("Time [s]")
plt.ylabel("Source IP")
plt.show()
print(df6_both_used)'''

# Normal use with both 
plt.figure(figsize=(20, 6))  
plt.title("Source IP used when browsing")
plt.plot(df3_udp_starlink["Time"], df3_udp_starlink["Source"], marker=".", linestyle="none")
plt.xlabel("Time [s]")
plt.ylabel("Source IP")
plt.gca().invert_yaxis()
plt.show()

colors = ['#ff7f0e', '#1f77b4']
plt.figure(figsize=(10, 6))  
plt.title("Source IP used when browsing")
counts = df3_udp_starlink["Source"].value_counts()
total = counts.sum()
percentages = counts / total * 100
percentages.plot(kind="pie", colors=colors, autopct="%.1f%%")
plt.ylabel("")  # remove y-label
plt.show()
print(df3_udp_starlink)
