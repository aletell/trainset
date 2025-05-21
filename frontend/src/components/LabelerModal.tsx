import React from 'react';
import Modal from 'react-modal';

const LabelerModal = ({ isOpen, onRequestClose, modalHeader, children, onOk, isFailed, isExport }) => {
  const handleOk = () => {
    onOk();
    onRequestClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Labeler Modal"
      className={`modalBox ${isExport ? 'exportBox' : 'defaultBox'}`}
      overlayClassName="Overlay"
    >
      <div className={`modalTitle ${isExport ? 'exportHeader' : 'defaultHeader'}`}>
        <h5 className="modalInfo">{modalHeader}</h5>
      </div>
      <div className={`modalContent dialog-content ${isExport ? 'exportContent' : 'defaultContent'}`}>
        {children}
      </div>
      <div className="modalBtnContainer">
        {!isFailed && (
          <button
            type="button"
            className={`btn btn-light modalBtn dualBtn ${isExport ? 'exportButton' : 'defaultButton'}`}
            onClick={onRequestClose}
          >
            {isExport ? 'Continue' : 'Cancel'}
          </button>
        )}
        <button
          type="button"
          className={`btn btn-light modalBtn ${isFailed ? 'singleBtn' : 'dualBtn'} ${isExport ? 'exportButton' : 'defaultButton'}`}
          onClick={handleOk}
        >
          {isExport ? 'Upload' : 'Ok'}
        </button>
      </div>
    </Modal>
  );
};

export default LabelerModal;
