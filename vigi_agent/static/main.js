const recordingVideoModal = document.getElementById('recording_video_modal');
if (recordingVideoModal) {
    recordingVideoModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget;

        // find parent element with class 'recording_date_section'
        const recordingDateSection = button.closest('.recording_date_section');

        // get data from the parent element
        const date = recordingDateSection.dataset.date;

        // find child element with class 'recording_video'
        const recordingVideo = button.querySelector('.recording_card');

        // get data from the child element
        const time = recordingVideo.dataset.time;

        // Update the modal's title
        const modalTitle = recordingVideoModal.querySelector('.modal-title')
        modalTitle.textContent = `Recording for ${date} at ${time}`;

        // find #video_source element among children of recording_video_modal
        const videoSource = recordingVideoModal.querySelector('#video_source');

        // update src attribute of the video source
        videoSource.src = `/recordings/${date}/${time}/video`;

        // find video element among children of recording_video_modal
        const video = recordingVideoModal.querySelector('video');

        // load and play the video
        video.load();
        video.play();
    });
}
