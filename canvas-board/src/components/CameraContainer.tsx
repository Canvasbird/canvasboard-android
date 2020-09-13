import { IonButton } from "@ionic/react";
import React, { useEffect, useRef, useState } from "react";
import "./CameraContainer.css";
// import { api } from "../config";
import Peer from "peerjs";

interface ContainerProps {}

const CameraContainer: React.FC<ContainerProps> = () => {
  const camRef: any = useRef();
  const streamRef: any = useRef();
  const peer: Peer = new Peer();
  const [classStarted, setClassStarted]: any = useState(true);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({
        video: { facingMode: { exact: "environment" } },
        audio: false,
      })
      .then((stream) => {
        camRef.current.srcObject = stream;
        camRef.current?.play();
        streamRef.current = stream;
      });

    // setInterval(() => {
    //   const ctx = canvasRef.current.getContext("2d");
    //   ctx.drawImage(
    //     camRef.current,
    //     0,
    //     0,
    //     canvasRef.current.width,
    //     canvasRef.current.height
    //   );
    // }, 10);
    return () => {
      camRef.current.srcObject.getTracks().forEach((track: any) => {
        track.stop();
      });
    };
  }, []);

  const connectPeer = () => {
    const call = peer.call("18jj1a0515000000", streamRef.current);
    call.on("stream", (stream) => {
      console.log(stream);
    });
    setClassStarted(false);
  };

  // const processImage = () => {
  //   // let frame = canvasRef.current.toDataURL("image/png");
  //   // fetch(`${api}/process`, {
  //   //   method: "POST",
  //   //   body: frame,
  //   // })
  //   //   .then((res) => {
  //   //     return res.json();
  //   //   })
  //   //   .then((data) => {
  //   //     imgRef.current.src = data["image"];
  //   //   });
  // };

  return (
    <div className="container">
      <video ref={camRef}></video>
      {classStarted ? (
        <IonButton onClick={connectPeer}>Connect</IonButton>
      ) : null}
    </div>
  );
};

export default CameraContainer;
