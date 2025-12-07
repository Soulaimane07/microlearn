import { configureStore } from "@reduxjs/toolkit";
import pipelinesReducer from "./slices/pipelinesSlice";
import datasetsReducer from "./slices/datasetsSlice";
import authReducer from "./slices/authSlice";

export const store = configureStore({
  reducer: {
    pipelines: pipelinesReducer,
    datasets: datasetsReducer,
    auth: authReducer
  }
});
