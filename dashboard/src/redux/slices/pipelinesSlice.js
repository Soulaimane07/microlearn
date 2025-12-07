import { createSlice } from "@reduxjs/toolkit";
import { pipelinesDataa } from "../../components/Variables";

const pipelinesSlice = createSlice({
  name: "pipelines",
  initialState: {
    list: pipelinesDataa
  },
  reducers: {
    addPipeline: (state, action) => {
      state.list.unshift(action.payload); // add new pipeline at the top
    },
    deletePipeline: (state, action) => {
      state.list = state.list.filter(p => p.id !== action.payload);
    },
    rerunPipeline: (state, action) => {
      state.list = state.list.map(p =>
        p.id === action.payload
          ? { ...p, status: "Queued", stepsCompleted: `0/${p.steps.length}` }
          : p
      );
    },
    stopPipeline: (state, action) => {
      state.list = state.list.map(p =>
        p.id === action.payload && p.status === "Running"
          ? { ...p, status: "Stopped" } // or "Failed" if you prefer
          : p
      );
    }
  }
});

export const { addPipeline, deletePipeline, rerunPipeline, stopPipeline } = pipelinesSlice.actions;
export default pipelinesSlice.reducer;
