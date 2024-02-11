import { Box } from "@mui/material";

export default function TrafficLight(props: any) {
  return (
    <Box
      sx={{
        borderRadius: "50%",
        width: "32px",
        height: "32px",
        backgroundColor: props.color,
      }}
    />
  );
}
