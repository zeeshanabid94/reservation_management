import React from 'react';
import PropTypes from 'prop-types';
import './form_text_input.css';
import './button.css'
export class FormTextInput extends React.Component {
    static propTypes = {
        key: PropTypes.string.isRequired,
        defaultValue: PropTypes.string.isRequired,
        onChange: PropTypes.func.isRequired,
        labelValue: PropTypes.string.isRequired
    }
    constructor(props) {
        super(props);

        this.state = {
            currentState: props.defaultValue
        }
    }
    

    render() {
        return (
            <div class="text_input">
                <label class="text_input_label">
                    {this.props.labelValue}
                </label>
                <input type="text" class="text_input_textbox" name={this.props.key} onChange={this.props.onChange}/>
            </div>
            
        )
    }
}

export class FormButton extends React.Component {
    static propTypes = {
        key: PropTypes.string.isRequired,
        onSubmit: PropTypes.func.isRequired,
        labelValue: PropTypes.string.isRequired
    }

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <button class="button" id={this.props.key} onClick={this.props.onSubmit}>
               {this.props.labelValue} 
            </button>
        )
    }
}