import os
import json
import pickle
import pprint as pp

import arrow

from mastodon import Mastodon
from bs4 import BeautifulSoup

def save(instance, toots):
    """
    Pickles toots
    Args:
        instance - used to identify pickles
        toots - to be pickled
    """
    file_path = os.path.join(".", "dontcommitmebro", instance + ".toots.pickle")
    with open(file_path, "wb") as f:
        pickle.dump(toots, f)

def load(instance):
    """
    Unpickles toots
    Args: instance - to load
    Returns: toots
    """
    file_path = os.path.join(".", "dontcommitmebro", instance + ".toots.pickle")
    with open(file_path, "rb") as f:
        return pickle.load(f)


def display_toots(instance):
    """
    keep for the formatting
    """
    toots = load(instance)
    print("no of toots: {}\n\n".format(len(toots)))
    for toot in toots:
        # print(json.dumps(toot))
        print("  {}  @{} {}".format(toot['account']['display_name'],
                                    toot['account']['username'],
                                    toot['created_at']))

        if toot['application'] is None:
            application = ''
        else:
            application = "via {}".format(toot['application']['name'])

        print("  ♺::{} ♥:{} id:{} {}".format(toot['reblogs_count'],
                                             toot['favourites_count'],
                                             toot['id'],
                                             application))

        soup = BeautifulSoup(toot['content'], "html.parser")
        toot_text = soup.get_text()
        print("  {} - {}\n".format(toot_text,
                                   toot['url']))

def get_secrets():
    """
    gets secrets

    returns: secret dict
    """
    home = os.environ['HOME']
    file_path = os.path.join(home, ".config.fifth_elephant")

    with open(file_path, 'r') as f:
        raw = f.read()

    secrets = json.loads(raw)

    if secrets is None:
        print("failed to parse config file!")
        os.sys.exit(-1)

    return secrets

def get_mastodon(instance,secrets):
    """
    gets an mastodon instance

    args: instance dict from get_secrets()
    returns: Mastodon instance
    """
    api_base_url="https://"+instance

    our_client_id = secrets[instance]["client_id"]
    our_client_secret = secrets[instance]["client_secret"]
    our_access_token = secrets[instance]["access_token"]
    return Mastodon(api_base_url=api_base_url, client_id=our_client_id,
                    client_secret=our_client_secret, access_token=our_access_token)


def cache_notifications(secrets):
    print("caching results")
    instances = list(secrets.keys())
    #instances = ["icosahedron.website"]
    for instance in instances:
        print(instance)
        mastodon = get_mastodon(instance, secrets)
        data = mastodon.notifications()
        save(instance, data)

def notifications():
    secrets = get_secrets()

    #cache_notifications(secrets)

    instances = list(secrets.keys())
    #instances = ['cybre.space','i.write.codethat.sucks'] # favs
    
    for instance in instances:
        print("//////////////////////////////////////////////////////////////////")
        print("// {}".format(instance))
        print("//////////////////////////////////////////////////////////////////\n")
        mastodon = get_mastodon(instance, secrets)
        data = load(instance)
        for item in data:
            note_type = item['type']
            if note_type == 'favourite':
                who = item['account']['acct']

                soup = BeautifulSoup(item['status']['content'], "html.parser")
                toot = soup.get_text()

                when = arrow.get(item['created_at']).humanize()

                print("  {} faved your status {}\n    {}\n".format(who, when, toot))
            elif note_type == 'follow':
                who = item['account']['display_name']
                handle = item['account']['acct']
                when = arrow.get(item['created_at']).humanize()

                print("  {} (@{}) followed you {}\n".format(who, handle, when))
            elif note_type == 'mention':
                who = item['account']['display_name']
                handle = item['account']['acct']
                when = arrow.get(item['created_at']).humanize()

                soup = BeautifulSoup(item['status']['content'], "html.parser")
                toot = soup.get_text()

                print("  {} (@{}) {}\n    {}\n".format(who, handle, when, toot))
            else:
                print("unhandled type: ", item['type'], "\n")
                pp.pprint(item)


if __name__ == '__main__':
    notifications()

