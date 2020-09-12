import { IonImg, IonButton } from "@ionic/react";
import React, { useEffect, useRef } from "react";
import "./CameraContainer.css";
import { api } from "../config";

interface ContainerProps {}

const CameraContainer: React.FC<ContainerProps> = () => {
  const camRef: any = useRef();
  const canvasRef: any = useRef();
  const imgRef: any = useRef();

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: { exact: "environment" } } })
      .then((stream) => {
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
    }, 10);
  }, []);

  const processImage = () => {
    let frame = canvasRef.current.toDataURL("image/png");
    fetch(`${api}/process`, {
      method: "POST",
      body: frame,
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        imgRef.current.src = data["image"];
      });
  };

  return (
    <div className="container">
      <video hidden ref={camRef}></video>
      <canvas height={500} width={500} ref={canvasRef}></canvas>
      <IonImg alt="" ref={imgRef} />
      <IonButton onClick={processImage}>Get Output</IonButton>
    </div>
  );
};

export default CameraContainer;
