---
id: video-agent
title: OpenSlate, keyframe review with the Director
width: 1440
height: 900
frame: Each study must show the conversation with the Director's latest message and both of its points, the selected shot's large preview, all three Scene 2 keyframes, and the action that confirms the frames and starts video, within one 1440×900 view.
must_contain: The Last Ferry | Harbour at dawn | Mara | maroon | 7.4
---
OpenSlate is a local video studio with a conversational director. A person develops a short film in conversation with the Director, an AI agent that writes the treatment, scenes and shots, generates a keyframe for each shot, and then generates video from the keyframes the person has reviewed. The conversation sits beside a workbench with Plan, Keyframes, Assets and Film views. This is the moment the Director has returned a scene's keyframes and is waiting for the person before it generates video. OpenSlate's current interface is not a constraint here; the visual direction is open.

Audience and scene: an independent filmmaker making a short for their own channel, at a desk with a large monitor, in a session of an hour or two. They move back and forth between talking to the Director and looking at frames. They care how each shot looks and do not want to read job status.

Business objective: video costs money and minutes for every shot, so nobody should start video from a frame they have not looked at, and a problem the Director has already noticed should be fixed in the keyframe, before video, not after. Today most regenerated video traces back to something that was visible in its keyframe.

What these filmmakers already use every day: a chat assistant, an image generator, and the timeline of a desktop video editor.

Products in this category: LTX Studio, Runway, Google Flow, Descript.

Content (fictional; use exactly, and do not add data):
- Project: "The Last Ferry", a 48-second short film, 16:9, 1920 × 1080, 30 fps. 3 scenes, 8 shots.
- Scene 1 "Closing time": 3 shots, video generated and saved.
- Scene 2 "Harbour at dawn": 3 shots. Keyframes for all three are back; no video yet.
  - 2.1 Wide. The empty harbour at dawn, the ferry moored, fog over the water. Motion: slow push-in. 5 s. Narration: none.
  - 2.2 Medium. Mara on the pier in her red coat, a ticket in her hand. Motion: static, her breath visible. 4 s. Narration: none.
  - 2.3 Close-up. The ticket's printed date, "Sunday 31 March", under Mara's thumb. Motion: slow tilt down. 6 s. Narration: "She'd kept the ticket for eleven years." The recorded line is 7.4 s.
- Scene 3 "Departure": 2 shots, not started.
- Conversation, latest at the bottom:
  - You, 10:42: "@Scene 2 make the harbour feel colder, more like early morning, and keep Mara's red coat."
  - Director, 10:44: "I rewrote the three Scene 2 prompts with a blue dawn light and kept Mara's red coat in 2.2. Keyframes for all three shots are back. Two things to check before I make video:"
    a. "In 2.2 the coat came out maroon rather than red. I kept it because the light is low; regenerate 2.2 if you want it brighter."
    b. "The narration for 2.3 is 7.4 seconds but the shot is 6 seconds. I suggest making 2.3 8 seconds, which moves Scene 3 two seconds later."
- Video for Scene 2 starts only after the person has opened each of its three current keyframes. Earlier keyframes and Scene 1's video are kept.
- Actions: reply to the Director; @ a scene or shot to point the conversation at it; select a shot; regenerate one shot's keyframe; edit a shot's prompt, motion, duration or narration; confirm Scene 2's frames and generate its video.
- No images are supplied and none may be faked. Show keyframes and the preview as labelled placeholders with the shot number and its one-line description. Do not invent costs, credits, model names, view counts or other projects.
- Standard app chrome that carries no data of its own is expected, as on any shipped screen: the project header, view tabs, a resize handle between conversation and workbench, playback controls, the message composer.

Representative state for every study: Keyframes view open, shot 2.1 selected and opened; 2.2 and 2.3 not opened yet; the Director's 10:44 message is the latest; nothing confirmed.
