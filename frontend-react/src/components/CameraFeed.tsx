const CameraFeed = () => {
    return (
        <div className="flex justify-center items-center">
            <img 
                src="http://localhost:8000/video_feed" 
                alt="Camera Feed" 
                className="rounded-lg shadow-lg"
            />
        </div>
    );
};

export default CameraFeed;
