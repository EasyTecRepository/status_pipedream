#!/usr/bin/env python3
# Coding by Easy Tec | easytec.tech
# Instructions may see on GitHub
# coded for pipedream code block (Python 3.12)
# version 2.0 (works)

import requests
import http.client
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def handler(pd):
    try:
        urls = [
            ('<service_url>', '<component_id>'),
            ('https://example.com', 'a1b2c3d4e5f6'),
            ('https://example.com', 'a1b2c3d4e5f6'),
            ('https://example.com', 'a1b2c3d4e5f6'),
            ('https://example.com', 'a1b2c3d4e5f6'),
            ('https://example.com', 'a1b2c3d4e5f6')
        ]
        
        unresolved_incidents = False
        unreachable_sites = []
        unreachable_sites_list = []
        status_details = []

        # Discord Webhook
        def sendDiscord():
            webhook = DiscordWebhook(url="<discord_webhook>", username="STATUSCHECK")

            embed = DiscordEmbed(title="MALFUNCTION REPORTED!", color="ffff00")
            embed.set_author(name="STATUSCHECK", url="<statuspage_url>", icon_url="https://img.icons8.com/ios-filled/1024/94D82D/progress-indicator.png", avatar_url="https://img.icons8.com/ios-filled/1024/94D82D/progress-indicator.png")
            embed.set_thumbnail(url="https://img.icons8.com/ios-filled/1024/FFBF00/error--v1.png")
            embed.add_embed_field(name="What next?", value="Please visit the following link for more details: <statuspage_url>")
            embed.set_footer(text="automatically generated message")
            embed.set_timestamp()

            webhook.add_embed(embed)
            response_discord = webhook.execute()

        # Status page API request
        url_statuspage = "https://api.statuspage.io/v1/pages/<page_id>/incidents/unresolved"
        headers_statuspage = {"Authorization": f"OAuth {'<api_key>'}"}
        response_statuspage = requests.get(url_statuspage, headers=headers_statuspage)
        
        if not response_statuspage.ok:
            print(f"Failed to fetch unresolved incidents from Statuspage API. Status code: {response_statuspage.status_code}")
            pd.export('continue_workflow', True)
            return
        
        # Review of unresolved incidents
        if len(response_statuspage.json()) != 0:
            print("Existing unresolved incidents. Stopping workflow.")
            unresolved_incidents = True
        
        # Review of the websites
        for url, incident_id in urls:
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                status_text = http.client.responses.get(response.status_code, 'Unknown Status')
                status_combined = f"{response.status_code} {status_text}"
                
                pd.export(f'status_{incident_id}', status_combined)

                if response.status_code != 200:
                    print(f"Website {url} returned status code: {response.status_code}. Continuing workflow.")
                    unreachable_sites.append(f'"{incident_id}":"partial_outage"')
                    unreachable_sites_list.append(str(incident_id))
                    status_details.append(status_combined)
            except requests.ConnectionError as e:
                status_combined = f"ConnectionError {str(e)}"
                pd.export(f'status_{incident_id}', 'Page not available')
                unreachable_sites.append(f'"{incident_id}":"major_outage"')
                unreachable_sites_list.append(str(incident_id))
                status_details.append('Page not available')
                print(f"Connection Error: {str(e)}. Continuing workflow.")
            except requests.Timeout:
                status_combined = "Request timed out"
                pd.export(f'status_{incident_id}', status_combined)
                unreachable_sites.append(f'"{incident_id}":"major_outage"')
                unreachable_sites_list.append(str(incident_id))
                status_details.append(status_combined)
                print(f"Request to {url} timed out. Continuing workflow.")
        
        # Creation of output variables in JSON format for use in the template
        components_json = {str(incident_id): "major_outage" for incident_id in unreachable_sites_list}
        component_ids_json = unreachable_sites_list
        
        # Convert the dictionary into a string
        unreachable_sites_string = (", ".join(unreachable_sites))
        unreachable_sites_string = unreachable_sites_string.strip('"')

        # Export of JSON variables for use in the template
        pd.export('unreachable_sites_string', unreachable_sites_string)
        #pd.export('unreachable_sites_list', json.dumps(component_ids_json)) # Hide output
        
        # Creation of the output variable for inaccessible websites in the old format
        if unresolved_incidents:
            unreachable_sites_str = ", ".join(unreachable_sites_list)
            pd.export('unreachable_sites_raw', unreachable_sites_str)
            pd.export('continue_workflow', False)
        elif unreachable_sites:
            unreachable_sites_str = ", ".join(unreachable_sites_list)
            pd.export('unreachable_sites_raw', unreachable_sites_str)
            pd.export('continue_workflow', True)
            sendDiscord()
        else:
            pd.export('unreachable_sites_raw', "")
            pd.export('continue_workflow', False)
        
        # Export of the status details of the affected services
        status_details_str = ", ".join(status_details)
        pd.export('status_details', status_details_str)

    except Exception as e:
        pd.export('status_text', str(e))
        pd.export('continue_workflow', True)
        print(f"Error occurred: {str(e)}. Continuing workflow.")
