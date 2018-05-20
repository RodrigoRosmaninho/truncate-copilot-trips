# truncate-copilot-trips

[CoPilot™ GPS](https://copilotgps.com) is a mobile GPS app that allows for the planning of road trips in advance. These trips consist of an ordered list of stops and are saved in **.trp** files.

CoPilot trips can also be made using some third-party tools which export to **.trp** such as the [Furkot Road Trip Planner](https://trips.furkot.com). In fact, people tend to plan their whole vacations in such tools, generating files containing well over 100 stops.

However, this poses problems, as it's much easier and more intuitive to have smaller files (one for each day for example) and also, the bigger the trip, the slower CoPilot gets at calculating routes.

---

Therefore, I made this Python tool that reads a **.trp** file, prints all the stops, and lets the user select a start and end points for the creation of a smaller file, while preserving the original. This way, a user can create 'sub-trips' of the main trip at will, making navigation easier and avoiding CoPilot slowdowns.

No breach of any copyright was intended
