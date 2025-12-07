// redux/slices/datasetsSlice.js
import { createSlice } from "@reduxjs/toolkit";
import { datasets as initialDatasets } from "../../components/Variables";


const datasetsSlice = createSlice({
  name: "datasets",
  initialState: { list: initialDatasets },
  reducers: {
    addDataset: (state, action) => {
      state.list.unshift(action.payload);
    },
    deleteDataset: (state, action) => {
      state.list = state.list.filter(d => d.id !== action.payload);
    },
  },
});

export const { addDataset, deleteDataset } = datasetsSlice.actions;
export default datasetsSlice.reducer;
