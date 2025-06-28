/**
 * Igual que la Card, se lo llama desde la view ue lo vaya a implementar y se le pasan los parámetros necesarios.
 * El children lo que hace es poder modelar la información que queramos adentro del modal, ver en el archivo que mandé
 */

import React from "react";
import '../Styles/Modal.css';

const Modal = ({onClose, children}) =>{
    return(
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e)=>e.stopPropagation()}>
                <button className="modal-close" onClick={onClose}>X</button>
                {children}
            </div>
        </div>
    )
}

export default Modal;
