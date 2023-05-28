from azure.data.tables import TableClient, UpdateMode
import requests

from DependencyList import riot_api_key, connection_string

def riot_wrapper(req, region):
    url = "https://" + region + ".api.riotgames.com/" + req + "?api_key=" + riot_api_key
    print(url)
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

table_client = TableClient.from_connection_string(connection_string, table_name="SchoolSummoner")

entity = table_client.get_entity(partition_key="pkey", row_key="rkey")
entities = table_client.query_entities(query_filter="")

for entity in entities:
    summonerid = entity["SummonerID"]
    region = entity["Region"]
    print(summonerid, region)
    league_info = riot_wrapper("lol/league/v4/entries/by-summoner/" + summonerid, region)
    unranked = True
    if league_info != None:
        for queue_info in league_info:
            if queue_info['queueType'] == "RANKED_SOLO_5x5":
                rank = queue_info['rank']
                tier = queue_info['tier']
                entity["Rank"] = rank
                entity["Tier"] = tier
                unranked = False
    if unranked:
        entity["Rank"] = "unranked"
        entity["Tier"] = ""
    print(entity["Rank"], entity["Tier"])
    table_client.update_entity(entity, mode=UpdateMode.MERGE)
