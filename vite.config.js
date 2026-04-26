.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem 1rem;
  background: #f5f5f3;
}

.card {
  width: 100%;
  max-width: 560px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e8e8e6;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.header h1 {
  font-size: 22px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #111;
}

.header p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #999;
}

.participants {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.participant-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid #ebebeb;
  border-radius: 10px;
  background: #fafafa;
}

.avatar-placeholder {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #f0f0ef;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 500;
  flex-shrink: 0;
}

.participant-info { flex: 1; min-width: 0; }
.participant-name { font-size: 14px; font-weight: 500; color: #111; }
.participant-sub { font-size: 12px; color: #999; margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.badge-connected {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 20px;
  background: #dcfce7;
  color: #15803d;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-outline {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}
.btn-outline:hover { background: #f5f5f3; }

.btn-add {
  font-size: 13px;
  color: #666;
  border: 1px dashed #ddd;
  background: transparent;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  width: 100%;
}
.btn-add:hover { background: #f5f5f3; }

.row-2 {
  display: flex;
  gap: 10px;
}

.field {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field label { font-size: 12px; color: #888; }

.field input {
  padding: 8px 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  color: #111;
  width: 100%;
}
.field input:focus { outline: none; border-color: #aaa; }

.btn-pill {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: white;
  color: #555;
  cursor: pointer;
  font-size: 13px;
}
.btn-pill:hover { background: #f5f5f3; }
.btn-pill.active { background: #111; color: white; border-color: #111; }

.error-msg {
  font-size: 13px;
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 8px 12px;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  flex: 1;
  padding: 11px;
  border-radius: 8px;
  background: #111;
  color: white;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.btn-primary:hover { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-secondary {
  padding: 11px 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: white;
  color: #333;
  font-size: 14px;
  cursor: pointer;
}
.btn-secondary:hover { background: #f5f5f3; }

.share-box {
  background: #f9f9f7;
  border: 1px solid #e8e8e6;
  border-radius: 10px;
  padding: 12px 14px;
}
.share-box p { font-size: 13px; color: #666; margin-bottom: 8px; }
.share-link-row { display: flex; gap: 8px; align-items: center; }
.share-link-row code { flex: 1; font-size: 11px; color: #333; word-break: break-all; }
.share-link-row button { font-size: 12px; padding: 4px 10px; border-radius: 6px; border: 1px solid #ddd; background: white; cursor: pointer; white-space: nowrap; }

.slots-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 340px;
  overflow-y: auto;
}

.slot-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 12px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
}

.slot-day { font-size: 13px; font-weight: 500; color: #15803d; min-width: 110px; }
.slot-time { font-size: 13px; color: #166534; flex: 1; }
.slot-dur { font-size: 12px; color: #4ade80; }

.empty-msg { font-size: 14px; color: #999; padding: 0.5rem 0; }
.more-msg { font-size: 13px; color: #999; text-align: center; padding: 6px 0; }

.btn-lettuce {
  width: 100%;
  margin-top: 10px;
  padding: 11px;
  border-radius: 8px;
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.btn-lettuce:hover { background: #dcfce7; }
