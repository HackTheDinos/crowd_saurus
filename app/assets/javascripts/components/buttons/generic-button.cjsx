React = require 'react'

module.exports = React.createClass
  displayName: 'GenericButton'

  getDefaultProps: ->
    label: 'Okay'

  render: ->
    classes = 'button'
    classes += " #{@props.className}" if @props.className?
      
    <button className = {classes} onClick={@props.onClick} >
      { @props.label }
    </button>