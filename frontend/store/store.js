import { configureStore } from "@reduxjs/toolkit";
import pipelineReducer from "./slices/pipelineSlice";

export const store = configureStore({
  reducer: {
    pipeline: pipelineReducer,
  },
});
