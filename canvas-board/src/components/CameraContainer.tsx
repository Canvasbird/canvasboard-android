import { IonImg } from "@ionic/react";
import React, { useEffect, useRef } from "react";
import "./CameraContainer.css";

interface ContainerProps {}

const CameraContainer: React.FC<ContainerProps> = () => {
  const camRef: any = useRef();
  const canvasRef: any = useRef();
  const imgRef: any = useRef();

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      camRef.current.srcObject = stream;
      camRef.current?.play();
    });

    setInterval(() => {
      const ctx = canvasRef.current.getContext("2d");
      ctx.drawImage(
        camRef.current,
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );

      let frame = canvasRef.current.toDataURL("image/png");
      fetch("http://localhost:5000/process", {
        method: "POST",
        body: frame,
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          imgRef.current.src = data["image"];
        });
    }, 120);
  }, []);

  return (
    <div className="container">
      <video hidden ref={camRef}></video>
      <canvas ref={canvasRef}></canvas>
      <IonImg ref={imgRef} />
    </div>
  );
};

export default CameraContainer;
