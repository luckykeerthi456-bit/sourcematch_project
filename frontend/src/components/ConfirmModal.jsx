import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

export default function ConfirmModal({ open, title = "Confirm", message, onConfirm, onCancel, confirmLabel = "Confirm", cancelLabel = "Cancel" }) {
  return (
    <Dialog open={!!open} onClose={onCancel} aria-labelledby="confirm-dialog-title">
      <DialogTitle id="confirm-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <Typography variant="body1">{message}</Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel} variant="outlined">
          {cancelLabel}
        </Button>
        <Button onClick={onConfirm} variant="contained" color="error">
          {confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
