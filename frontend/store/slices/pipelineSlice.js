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
    processed: null,
    status: "idle", // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
  },
  reducers: {
    resetPipeline: (state) => {
      state.pipeline = null;
      state.status = "idle";
      state.error = null;
    },
    setProcessedData: (state, action) => {
      state.processed = action.payload;
    }
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

export const { resetPipeline, setProcessedData } = pipelineSlice.actions;
export default pipelineSlice.reducer;
