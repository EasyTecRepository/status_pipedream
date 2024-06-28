# Statuscheck with Pipedream.com
![Error](https://github.com/EasyTecRepository/status_pipedream/blob/main/images/Thumbnail_GitHub.png?raw=true)

## What is this?
This is a simple script that can check the current status of your services and create an incident on the status page if necessary.
All this works via Python scripts and the website pipedream.com.

> [!NOTE]
> This is not an advertisement!

## Wait, pipedream.com, what's that and why I use this?
With pipedream.com you have the possibility to run scripts on an external server. This is necessary, for example, if your home server is not available or you have problems with your network connection.

> [!IMPORTANT]
> In the **free version** of Pipedream.com, it is only possible to **run** the check **script** a **maximum** of **10 times a day**. This means that it can only be executed **every 2.5 hours**.

## Why do I need that?
Because you want to know when your services are offline. So this is a must for anyone who has a few services to maintain.

## How do I get it?
Watch this [tutorial on YouTube (german)](https://youtube.com/EasyTec100) or read the following guide.

## The guide (step-by-step)
1. Create an account [here](https://pipedream.com/auth/signup)
2. Login and First Setup
3. Go to `Projects` => `New project`
4. Set name and click `Create Project`
5. Click `New` => `Workflow`
6. Set name and click `Create Workflow`
7. Click `Add Trigger`
8. Click `Custom Interval`
9. Set `Every 150 Minutes`
10. Click `Save and Continue`
11. Click on `+`
12. Search after `Python` => select `Run Python code` (
13. Paste [this Code](pipedream_code_block.py) into the Code section
14. Adjust all variables

| Quantity | Variable          | Explanation                   | Example                                                                     |
| :------: | :---------------: | :---------------------------: | :-------------------------------------------------------------------------- |
| 1        | <service_url>     | URL of your Websites          | https://example.com                                                         |
| 1        | <component_id>    | Component_id to your Websites | a1b2c3d4e5f6                                                                |
| 1        | <discord_webhook> | Discord Webhook URL           | https://discord.com/api/webhooks/12345678910/ABCdEFG_hIJKlMNOp_QRsTUVw_XYz/ |
| 2        | <statuspage_url>  | URL of your statuspage        | https://atlassian.statuspage.io/                                            |
| 1        | <page_id>         | PageID of your statuspage     | 12ab34cd56ef                                                                |
| 1        | <api_key>         | API_Key from statuspage       | 123abc456def789ghi1011jkl1213mno                                            |

15. Click `Test`
16. Click `+` and select `Continue execution if a condition is met` (Actions -> Control Flow)
17. Set `Initial Value` to `{{steps.code.continue_workflow}}`
18. Set `Condition` to `Text Matches exactly (TEXT_EQUALS)`
19. Set `Second value` to `true`
20. By `Case sensitive` click on `CLEAR`
21. Click `Test`
22. Click `+`, click `HTTP / Webhook` and select `Send POST Request`
23. Set `Request URL` to `https://api.statuspage.io/v1/pages/<your_page_id>/incidents/` (INSERT YOUR PAGE ID!!)
24. Set `Authorization Type` to `Bearer Token` and insert your API Key from Statuspage
25. Click on `Body` and insert [this JSON code](pipedream_create_incident.json)
26. Click on `Test`
27. Click on `Deploy`
The workflow should now be executed automatically every 150 minutes to check the status of your specified services to create an incident on the Statuspage if necessary.

## sources
[Error](https://icons8.com/icon/8122/error) icon by [Icons8](https://icons8.com)

[Fortschrittsanzeige](https://icons8.com/icon/108535/fortschrittsanzeige) icon by [Icons8](https://icons8.com)
