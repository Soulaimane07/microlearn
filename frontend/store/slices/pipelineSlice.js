import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { OrchestratorUrl } from "../../components/variables";

// Async thunk to fetch pipeline status
export const fetchPipeline = createAsyncThunk(
  "pipeline/fetchPipeline",
  async (pipelineId) => {
    const res = await fetch(`${OrchestratorUrl}/pipeline/status/${pipelineId}`);
    const data = await res.json();
    return data;
  }
);

const pipelineSlice = createSlice({
  name: "pipeline",
  initialState: {
    pipeline: null,
    datapreparer: null,
    modelselection: null,
    trainer: null,
    modelevaluation: null,
    status: "idle", 
    error: null,
  },
  reducers: {
    resetPipeline: (state) => {
      state.pipeline = null;
      state.status = "idle";
      state.error = null;
    },
    storedatapreparer: (state, action) => {
      state.datapreparer = action.payload;
    },
    storemodelselection: (state, action) => {
      state.modelselection = action.payload;
    },
    storetrainer: (state, action) => {
      state.trainer = action.payload;
    },
    storemodelevaluation: (state, action) => {
      state.modelevaluation = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPipeline.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchPipeline.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.pipeline = action.payload;
      })
      .addCase(fetchPipeline.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      });
  },
});

export const { resetPipeline, storedatapreparer, storemodelselection, storetrainer, storemodelevaluation } = pipelineSlice.actions;
export default pipelineSlice.reducer;
