---
name: editorial-film-edit
description: Edit footage in an archival editorial style with bundled video and photo references, kinetic text, film grain, bloom, masks and presenter splits. Use for new edits and final visual revisions.
---

# Editorial film edit

Assemble and refine real videos in a soft archival editorial style. The style adapts to any topic, presenter, duration and format. Communicate in the user's language; English is required only for generation prompts, if generation is needed.

## Bundled materials

All permanent references are already included in the skill. Do not ask for them to be uploaded as separate attachments or for the package author's finished work to be sent. Social media links provide provenance and additional guidance; access to them is not required to view the local copies.

Before a new edit:

1. Read [style-guide.md](references/style-guide.md): composition, grain, bloom, B&W, fonts, motion, masks, splits and sound.
2. Read [reference-map.md](references/reference-map.md). Open the four bundled photographs and four frame overviews; to study animation, examine the local MP4s or frame sequences in the specified time windows. Motion cannot be determined from a cover image. All four MP4s are silent; they cannot establish what music the originals use.
3. For revisions, also read [revision-checklist.md](references/revision-checklist.md) and review the latest version belonging to the current user.
4. When using the included modules, first read [implementation-guide.md](references/implementation-guide.md). These are implementation examples for individual layers, not a ready-to-run project. Their default values do not replace the style guide.

Media are in `references/photos/`, `references/videos/`, `references/frames/`; [media-manifest.json](references/media-manifest.json) contains paths, provenance and checksums. The local examples demonstrate motion and materials, but do not grant permission to automatically include them as B-roll in a new video.

## New project

The new user-provided source is the basis for the content. Unless otherwise specified, preserve its duration, clip order, speech, pauses, aspect ratio and original sound. Choose the frame rate/export settings based on the actual source; do not increase resolution without a reason. For long videos, reduce the density of inserts and allow time for viewing and reading. If there is no presenter or speech, adapt the compositional language to the action; speech captions and presenter splits are not needed.

Create a new transcript, source-to-programme time map, frames, captions, masks and assets. Neither the examples' duration nor their people, text, scenes or completed reports are content templates. Account for cuts between takes already baked into the source: do not reveal stray frames from an adjacent take when returning from B-roll. When shifting a shot boundary, preserve the absolute timing of spoken words. Do not copy historical timelines, masks, opening-frame caches or music.

The references define the visual grammar, and the style guide defines the requirements for combining it. Select archival objects and metaphors for the new topic. CRTs, computing machines and laboratories belong to technology stories, not every video. Names, numbers, real interfaces and quotations must match the source. Clarify an important unintelligible phrase rather than inventing it.

## Environment and workflow

Before promising an MP4, verify access to the new source, decoding of its picture/audio, and the availability of export tools, the required fonts and mask processing. The skill does not install a video editor, system fonts or access to third-party services. If an essential capability is unavailable, state exactly what is missing and the minimum way to proceed; do not present HTML, code or a plan as a finished video. If the ZIP is accessible only as a text listing, an environment with access to its extracted resources is required, not another upload of dozens of attachments.

Use a working copy in an accessible project folder; the installed skill directory may be read-only. Do not change its files during routine editing. Any available renderer that produces the required image and controllable layers is acceptable. When the tools are available, perform the edit rather than stopping at recommendations.

Briefly describe the direction, then continue assembling independently. Ask only about blocking assets/decisions and required permissions. Make short tests with light and dark B-roll, B&W, typography, a split and a mask before an expensive full export. Work from clean layers: source, inserts, text, masks, sound. Preserve the previous version when making revisions.

For B-roll, use supplied assets and suitable sources with clear usage terms; retain provenance and required credits. Pinterest alone does not establish usage rights. Describe the status of viewed links honestly. If several new illustrative shots are needed and Higgsfield/Seedance 2.5 are available with an agreed budget, prepare detailed English prompts in the current project: subject, composition, material, light, optics, one movement, and space for text. Generation is optional; if unavailable, use suitable accessible sources. Do not silently substitute the model or present generated imagery as historical evidence. Publication, messages to third parties and spending money do not automatically follow from using this skill.

## Final result

Check the new export itself: grain and text motion, both sides of transitions, mask edges, legibility at the target size, synchronization, sound, and the absence of missing media, unwanted black/frozen frames, bars and stretching. Check duration, fps, dimensions, decoding and caption bounds. Contact sheets and numerical metrics help, but do not replace watching motion and listening. Do not report an unperformed check as passed.

Fix actual defects and recheck the changed areas. If a missing capability or external limit blocks progress, stop the dependent operation with a precise explanation; endless retries are not quality assurance.

Deliver the MP4, an editable project with the assets used or an exact list of external dependencies, sources, and a brief description of the actual changes/limitations. If music was added, also deliver a version without it. If only the picture changed and the duration stayed the same, preserve the approved sound. Store style parameters separately from the project's specific media and timecodes. Update the skill itself only at the user's request.
