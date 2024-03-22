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

        // get data and camera_id from the child element
        const time = recordingVideo.dataset.time;
        const camera_id = recordingVideo.dataset.cameraId;

        // Update the modal's title
        const modalTitle = recordingVideoModal.querySelector('.modal-title')
        modalTitle.textContent = `Recording for ${date} at ${time} from camera #${camera_id}`;

        // find #video_source element among children of recording_video_modal
        const videoSource = recordingVideoModal.querySelector('#video_source');

        // update src attribute of the video source
        videoSource.src = `/recordings/${camera_id}/${date}/${time}/video`;

        // update download link
        const downloadLink = recordingVideoModal.querySelector('#download_link');
        downloadLink.href = `/recordings/${camera_id}/${date}/${time}/video?download=true`;

        // update share link
        const shareLink = recordingVideoModal.querySelector('#share_link');
        shareLink.href = `/recordings/${camera_id}/${date}/${time}/video?share=true`;

        // update delete link
        const deleteLink = recordingVideoModal.querySelector('#delete_link');
        deleteLink.href = `/recordings/${camera_id}/${date}/${time}/delete`;

        // find video element among children of recording_video_modal
        const video = recordingVideoModal.querySelector('video');

        // read tags and update the tags element
        const tagsElement = recordingVideoModal.querySelector('#tags');

        // remove all children from #tags element
        while (tagsElement.firstChild) {
            tagsElement.removeChild(tagsElement.firstChild);
        }

        // split tags by comma
        const tags = recordingVideo.dataset.tags.split(',');
        
        // for each tag in tags create a span with badge bg-secondary classes and
        // append it to the tagsElement element
        tags.forEach(tag => {
            const span = document.createElement('span');
            span.className = "badge text-bg-info ms-1";
            span.textContent = tag;
            tagsElement.appendChild(span);
        });

        // load and play the video
        video.load();
        video.play();
    });
}

// handle the click event on the share_link
const shareLink = document.getElementById('share_link');
if (shareLink) {
    shareLink.addEventListener('click', event => {
        // prevent the default action
        event.preventDefault();

        // use navigator.share if available
        if (navigator.share) {
            navigator.share({
                title: 'Vigi Agent',
                text: 'Check out this video',
                url: event.target.href,
            })
            .then(() => console.log('Successful share'))
            .catch((error) => console.log('Error sharing', error));
        } else {
            // if navigator.share is not available, copy the link to the clipboard
            navigator.clipboard.writeText(event.target.href)
            .then(() => alert('Link copied to clipboard'))
        }
    });
}

// handle delete_link click event
const deleteLink = document.getElementById('delete_link');
if (deleteLink) {
    deleteLink.addEventListener('click', event => {
        // ask for a confirmation
        if (!confirm('Are you sure you want to delete this recording?')) {
            // if the user clicks cancel, return
            return;
        }

        // prevent the default action
        event.preventDefault();

        // send a DELETE request to the link's href
        fetch(event.target.href, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert('Recording deleted successfully');
                location.reload();
            } else {
                alert('An error occurred while deleting the recording');
            }
        });
    });
}

const liveVideoModal = document.getElementById('live_video_modal');
if (liveVideoModal) {
    liveVideoModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget;

        // find a child element with class 'live_view_img'
        // copy src attribute of the img element
        const src = button.querySelector(".live_view_img").src

        // update src of #live_video_modal_img
        const liveVideoModalImg = liveVideoModal.querySelector('#live_video_modal_img');
        liveVideoModalImg.src = src;

        // update modal title
        const modalTitle = liveVideoModal.querySelector('#modalTitle');
        const card_title = button.querySelector('.card-title');
        modalTitle.textContent = `Live view from ${card_title.textContent}`;
    });
}
