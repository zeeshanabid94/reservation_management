import React from 'react';
import Proptypes from 'prop-types';
import '../../App.css'
import './modal.css'

export class Modal extends React.Component {
    static propTypes = {
        show: Proptypes.bool.isRequired,
        children: Proptypes.array.isRequired,
        heading: Proptypes.array.isRequired,
        onClose: Proptypes.func.isRequired
    }

    constructor(props) {
        super(props);
    }

    render() {
        console.log("Modal State", this.state);
        console.log("Modal Props", this.props);
        return (
            <div class={this.props.show === true ? 'modal_box modal_open':'modal_box modal_closed'}>
                <div class="modal">
                    <div class="close_icon" onClick={this.props.onClose}>
                        X
                    </div>
                    <h2 class="modal_heading">
                        {this.props.heading}
                    </h2>
                    <form>
                        <div class="modal_content">
                            {this.props.children}
                        </div>
                    </form>
                    
                </div>
            </div>
            
        )
    }
}